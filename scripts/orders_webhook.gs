/**
 * Khafeefa - Orders webhook for Google Sheets
 *
 * Replace SPREADSHEET_ID below with the ID from your sheet URL:
 *   https://docs.google.com/spreadsheets/d/<<SPREADSHEET_ID>>/edit
 *
 * Deployment steps:
 *   1. Open the sheet → Extensions → Apps Script (or use this standalone script).
 *   2. Paste this ENTIRE file (replace any existing code).
 *   3. Save (disk icon). Project name: "Khafeefa Orders Webhook".
 *   4. Deploy → New deployment → gear icon → Web app.
 *        - Description: orders
 *        - Execute as: Me
 *        - Who has access: Anyone
 *      Click Deploy → Authorize when prompted.
 *   5. Copy the Web app URL (ends with /exec) and paste it into the backend env:
 *        ORDER_WEBHOOK_URL=https://script.google.com/macros/s/.../exec
 *
 * If you edit this script later, ALWAYS:
 *   Deploy → Manage deployments → pencil icon → Version: New version → Deploy.
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

function doGet(e) {
  return jsonResponse_({
    ok: true,
    message: "Khafeefa orders webhook is live.",
    spreadsheet_id: SPREADSHEET_ID,
    sheet: SHEET_NAME
  });
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(30000);
  } catch (err) {
    return jsonResponse_({ ok: false, error: "LOCK_TIMEOUT: " + err.message });
  }

  try {
    const body = (e && e.postData && e.postData.contents) ? e.postData.contents : "{}";
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

    return jsonResponse_({
      ok: true,
      order_id: data.order_id || null,
      appended_row: sheet.getLastRow()
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

function getOrCreateSheet_() {
  // Always open the spreadsheet by ID so this works whether the script is
  // bound to a sheet or standalone.
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
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
