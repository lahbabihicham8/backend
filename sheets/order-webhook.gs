const CONFIG = {
  ORDERS_SHEET: 'orders',
  ITEMS_SHEET: 'order_items',
  EVENTS_SHEET: 'events',
};

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);

  try {
    const payload = JSON.parse(e.postData.contents || '{}');
    const secret = PropertiesService.getScriptProperties().getProperty('ORDER_WEBHOOK_SECRET');
    const providedSecret = payload.secret || '';

    if (!secret || providedSecret !== secret) {
      return json_({ ok: false, error: 'UNAUTHORIZED' });
    }

    if (payload.type === 'order_created' || payload.type === 'order_updated') {
      appendOrder_(payload.order || {});
      (payload.items || []).forEach(function(item) {
        appendItem_(payload.order || {}, item || {});
      });
      return json_({ ok: true });
    }

    if (payload.type === 'event_log') {
      appendEvent_(payload.event || {});
      return json_({ ok: true });
    }

    return json_({ ok: false, error: 'UNKNOWN_TYPE' });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function appendOrder_(order) {
  const sheet = getSheet_(CONFIG.ORDERS_SHEET);
  sheet.appendRow([
    order.order_id || '',
    order.order_number || '',
    order.created_at || '',
    order.customer_name || '',
    order.phone_e164 || '',
    order.phone_raw || '',
    order.status || '',
    order.currency || '',
    order.subtotal || '',
    order.total || '',
    order.payment_method || '',
    order.client_ip || '',
    order.country || '',
    order.fraud_decision || '',
    order.fraud_reason || '',
    order.maxmind_risk_score || '',
    order.utm_source || '',
    order.utm_medium || '',
    order.utm_campaign || '',
    order.utm_content || '',
    order.utm_term || '',
    order.event_id || '',
  ]);
}

function appendItem_(order, item) {
  const sheet = getSheet_(CONFIG.ITEMS_SHEET);
  sheet.appendRow([
    order.order_id || '',
    order.order_number || '',
    item.product_id || '',
    item.offer_id || '',
    item.title || '',
    item.quantity || '',
    item.unit_price || '',
    item.total_price || '',
    item.is_upsell === true ? 'true' : 'false',
  ]);
}

function appendEvent_(event) {
  const sheet = getSheet_(CONFIG.EVENTS_SHEET);
  sheet.appendRow([
    event.created_at || '',
    event.order_id || '',
    event.platform || '',
    event.event_name || '',
    event.event_id || '',
    event.success === true ? 'true' : 'false',
    event.status_code || '',
    event.message || '',
  ]);
}

function getSheet_(name) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
  if (!sheet) {
    throw new Error('Missing sheet: ' + name);
  }
  return sheet;
}

function json_(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
