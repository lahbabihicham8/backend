/**
 * Khafeefa - Orders webhook for Google Sheets
 *
 * Handles BOTH payload shapes:
 *   - New flat shape: { date, order_id, country, name, phone, product,
 *                       sku, quantity, total_price, currency, status }
 *   - Old wrapped shape: { secret?, order: { order_number, customer_name,
 *                          phone_raw, total, currency, items: [...] } }
 *
 * Deployment:
 *   1. Paste this ENTIRE file into Apps Script editor.
 *   2. Save (disk icon).
 *   3. Deploy → Manage deployments → pencil icon → Version: New version → Deploy.
 *   4. The Web app URL stays the same.
 */

const SPREADSHEET_ID = "11r-5mqiZaPJ2IiqcTrTDaV6jcVT8GmtH6p9cR8cjXdo";
const SHEET_NAME = "Orders";

const HEADERS = [
  "date",
  "order_id",
  "country",
  "name",
  "phone",
  "product",
  "sku",
  "quantity",
  "total_price",
  "currency",
  "status"
];

// Map product_id → Arabic name and stable SKU. Add new products here.
const PRODUCT_CATALOG = {
  "khafeefa-waist-fan-powerbank": {
    title: "مروحة خفيفة للخصر مع باور بانك",
    sku: "KH-WF-PB-001"
  }
};

function doGet(e) {
  // Dump current sheet contents so Cursor can read the rows directly.
  try {
    const sheet = getOrCreateSheet_();
    const values = sheet.getDataRange().getValues();
    return jsonResponse_({
      ok: true,
      message: "Khafeefa orders webhook is live.",
      spreadsheet_id: SPREADSHEET_ID,
      sheet: SHEET_NAME,
      row_count: values.length,
      rows: values
    });
  } catch (err) {
    return jsonResponse_({
      ok: false,
      error: String(err && err.message ? err.message : err)
    });
  }
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  try { lock.waitLock(30000); }
  catch (err) { return jsonResponse_({ ok: false, error: "LOCK_TIMEOUT: " + err.message }); }

  try {
    const body = (e && e.postData && e.postData.contents) ? e.postData.contents : "{}";
    const data = JSON.parse(body);
    const row = buildRow_(data);

    const sheet = getOrCreateSheet_();
    sheet.appendRow([
      row.date, row.order_id, row.country, row.name, row.phone,
      row.product, row.sku, row.quantity, row.total_price,
      row.currency, row.status
    ]);

    return jsonResponse_({
      ok: true,
      order_id: row.order_id || null,
      appended_row: sheet.getLastRow(),
      shape_detected: data && data.order ? "wrapped" : "flat"
    });
  } catch (err) {
    return jsonResponse_({
      ok: false,
      error: String(err && err.message ? err.message : err),
      stack: String(err && err.stack ? err.stack : "")
    });
  } finally {
    try { lock.releaseLock(); } catch (e) {}
  }
}

/** Build a normalized row from either payload shape. */
function buildRow_(data) {
  // Detect old wrapped format: { secret?, order: {...} }
  if (data && data.order && typeof data.order === "object") {
    return buildRowFromOrder_(data.order);
  }

  // New flat format - just take fields as-is, fall back to sensible defaults.
  return {
    date: data.date || todayDdMmYyyy_(),
    order_id: data.order_id || "",
    country: data.country || "Kuwait",
    name: data.name || "",
    phone: data.phone || "",
    product: data.product || "",
    sku: data.sku || "",
    quantity: data.quantity || "",
    total_price: data.total_price != null ? String(data.total_price) : "",
    currency: data.currency || "KWD",
    status: data.status || ""
  };
}

function buildRowFromOrder_(order) {
  const items = Array.isArray(order.items) ? order.items : [];
  const products = items.map(function (it) { return arabicNameFor_(it); });
  const skus = items.map(function (it) { return skuFor_(it.product_id); });
  const quantities = items.map(function (it) {
    var q = it.quantity;
    return q == null ? "" : String(parseInt(q, 10) || q);
  });

  return {
    date: formatDate_(order.created_at) || todayDdMmYyyy_(),
    order_id: order.order_number || order.order_id || "",
    country: "Kuwait",
    name: order.customer_name || "",
    phone: formatPhone_(order),
    product: products.join("/"),
    sku: skus.join("/"),
    quantity: quantities.join("/"),
    total_price: order.total != null ? String(order.total) : "",
    currency: "KWD",
    status: ""
  };
}

function arabicNameFor_(item) {
  if (!item) return "";
  var entry = PRODUCT_CATALOG[item.product_id];
  if (entry && entry.title) return entry.title;
  return item.title || item.product_id || "";
}

function skuFor_(productId) {
  var entry = PRODUCT_CATALOG[productId];
  if (entry && entry.sku) return entry.sku;
  return "KH-PROD";
}

/** Format a Kuwait phone as "96550475233" (no +, country code prefixed). */
function formatPhone_(order) {
  var e164 = (order.phone_e164 || "").replace(/^\+/, "");
  if (e164) return e164;

  var raw = (order.phone_raw || "").replace(/\D/g, "");
  if (!raw) return "";
  if (raw.indexOf("965") === 0) return raw;
  return "965" + raw;
}

/** Convert an ISO timestamp (or anything Date parses) to dd/MM/yyyy. */
function formatDate_(value) {
  if (!value) return "";
  try {
    var d = new Date(value);
    if (isNaN(d.getTime())) return "";
    return pad_(d.getDate()) + "/" + pad_(d.getMonth() + 1) + "/" + d.getFullYear();
  } catch (e) {
    return "";
  }
}

function todayDdMmYyyy_() {
  var d = new Date();
  return pad_(d.getDate()) + "/" + pad_(d.getMonth() + 1) + "/" + d.getFullYear();
}

function pad_(n) {
  return n < 10 ? "0" + n : "" + n;
}

function getOrCreateSheet_() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold");
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function jsonResponse_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
