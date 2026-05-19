/**
 * Khafeefa - Orders webhook for Google Sheets
 *
 * Deployment:
 *   1. Open the orders sheet → Extensions → Apps Script.
 *   2. Delete the default code and paste this entire file.
 *   3. Click Save (disk icon). Project name: "Khafeefa Orders Webhook".
 *   4. Deploy → New deployment → Select type: Web app.
 *        - Description: orders
 *        - Execute as: Me
 *        - Who has access: Anyone
 *      Click Deploy → Authorize when prompted.
 *   5. Copy the "Web app URL" (ends with /exec) and put it in the backend env:
 *        ORDER_WEBHOOK_URL=https://script.google.com/macros/s/.../exec
 *   6. Redeploy the backend service in EasyPanel.
 *
 * After this, every new order automatically appends one row.
 */

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

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const body = e && e.postData && e.postData.contents ? e.postData.contents : "{}";
    const data = JSON.parse(body);

    const sheet = getOrCreateSheet_();

    sheet.appendRow([
      data.date || "",
      data.order_id || "",
      data.country || "Kuwait",
      data.name || "",
      data.phone || "",
      data.product || "",
      data.sku || "",
      data.quantity || "",
      data.total_price || "",
      data.currency || "KWD",
      data.status || ""
    ]);

    return jsonResponse_({ ok: true });
  } catch (err) {
    return jsonResponse_({ ok: false, error: String(err && err.message || err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService
    .createTextOutput("Khafeefa orders webhook is live.")
    .setMimeType(ContentService.MimeType.TEXT);
}

function getOrCreateSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
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
