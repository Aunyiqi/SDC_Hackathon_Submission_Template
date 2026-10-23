(() => {
  const byId = (id) => document.getElementById(id);
  const form = byId('supplierCheckForm');
  if (!form) return;

  const fields = {
    poQuantity: byId('po_quantity'),
    poUnit: byId('po_unit'),
    poPrice: byId('po_price'),
    receivedQuantity: byId('received_quantity'),
    receivedUnit: byId('received_unit'),
    invoiceQuantity: byId('invoice_quantity'),
    invoiceUnit: byId('invoice_unit'),
    invoicePrice: byId('invoice_price')
  };

  const preview = {
    state: byId('previewState'),
    stateText: byId('previewStateText'),
    units: byId('previewUnits'),
    quantity: byId('previewQuantity'),
    price: byId('previewPrice'),
    receivedAmount: byId('previewReceivedAmount'),
    invoiceAmount: byId('previewInvoiceAmount'),
    difference: byId('previewDifference')
  };

  const parseNumber = (input) => {
    const value = Number.parseFloat(input?.value ?? '');
    return Number.isFinite(value) ? value : null;
  };

  const normalizeUnit = (input) => (input?.value ?? '').trim().toLowerCase();
  const money = (value) => value === null ? '—' : `RM${value.toFixed(2)}`;
  const almostEqual = (a, b) => Math.abs(a - b) < 0.0001;

  function setState(level, text) {
    preview.state.className = `preview-state preview-${level}`;
    preview.stateText.textContent = text;
  }

  function updatePreview() {
    const poQty = parseNumber(fields.poQuantity);
    const receivedQty = parseNumber(fields.receivedQuantity);
    const invoiceQty = parseNumber(fields.invoiceQuantity);
    const poPrice = parseNumber(fields.poPrice);
    const invoicePrice = parseNumber(fields.invoicePrice);
    const poUnit = normalizeUnit(fields.poUnit);
    const receivedUnit = normalizeUnit(fields.receivedUnit);
    const invoiceUnit = normalizeUnit(fields.invoiceUnit);

    const numbersReady = [poQty, receivedQty, invoiceQty, poPrice, invoicePrice].every((value) => value !== null);
    const unitsReady = [poUnit, receivedUnit, invoiceUnit].every(Boolean);

    if (!numbersReady || !unitsReady) {
      setState('waiting', 'Complete the evidence fields to preview the check.');
      preview.units.textContent = unitsReady ? 'Entered' : 'Waiting for units';
      preview.quantity.textContent = 'Waiting for values';
      preview.price.textContent = 'Waiting for values';
      preview.receivedAmount.textContent = '—';
      preview.invoiceAmount.textContent = '—';
      preview.difference.textContent = '—';
      return;
    }

    const unitsComparable = poUnit === receivedUnit && poUnit === invoiceUnit;
    if (!unitsComparable) {
      setState('blocked', 'Clarification required — units are not directly comparable.');
      preview.units.textContent = `${poUnit} / ${receivedUnit} / ${invoiceUnit}`;
      preview.quantity.textContent = 'Not compared until units are clarified';
      preview.price.textContent = almostEqual(poPrice, invoicePrice) ? 'Price matches PO' : `Invoice price differs by RM${Math.abs(invoicePrice - poPrice).toFixed(2)} / ${poUnit}`;
      preview.receivedAmount.textContent = '—';
      preview.invoiceAmount.textContent = money(invoiceQty * invoicePrice);
      preview.difference.textContent = 'Blocked';
      return;
    }

    const receivedAmount = receivedQty * poPrice;
    const invoiceAmount = invoiceQty * invoicePrice;
    const difference = invoiceAmount - receivedAmount;
    const quantityIssues = [];

    if (!almostEqual(poQty, receivedQty)) {
      const delta = receivedQty - poQty;
      quantityIssues.push(`${Math.abs(delta).toFixed(2)} ${poUnit} ${delta < 0 ? 'short received' : 'over received'}`);
    }
    if (!almostEqual(invoiceQty, receivedQty)) {
      const delta = invoiceQty - receivedQty;
      quantityIssues.push(`invoice differs from received by ${Math.abs(delta).toFixed(2)} ${poUnit}`);
    }

    const priceIssue = !almostEqual(poPrice, invoicePrice);
    const hasIssue = quantityIssues.length > 0 || priceIssue;

    setState(
      hasIssue ? 'review' : 'clear',
      hasIssue ? 'Review likely — browser preview found a discrepancy.' : 'Looks consistent — server will verify after submission.'
    );
    preview.units.textContent = `Comparable (${poUnit})`;
    preview.quantity.textContent = quantityIssues.length ? quantityIssues.join(' · ') : 'PO, received and invoice quantities align';
    preview.price.textContent = priceIssue ? `Invoice price differs by RM${Math.abs(invoicePrice - poPrice).toFixed(2)} / ${poUnit}` : 'Invoice price matches agreed price';
    preview.receivedAmount.textContent = money(receivedAmount);
    preview.invoiceAmount.textContent = money(invoiceAmount);
    preview.difference.textContent = money(Math.abs(difference));
  }

  Object.values(fields).forEach((field) => {
    field?.addEventListener('input', updatePreview);
    field?.addEventListener('change', updatePreview);
  });

  const button = byId('extractButton');
  const status = byId('extractStatus');
  if (button && status) {
    button.addEventListener('click', async () => {
      button.disabled = true;
      status.textContent = 'Extracting…';
      try {
        const response = await fetch('/api/extract', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message: byId('supplier_message').value})
        });
        const result = await response.json();
        if (!result.ok) {
          status.textContent = result.error;
          return;
        }
        const data = result.data;
        if (data.item) byId('item').value = data.item;
        if (data.quantity !== null && data.quantity !== undefined) fields.receivedQuantity.value = data.quantity;
        if (data.unit) fields.receivedUnit.value = data.unit;
        if (data.unit_price !== null && data.unit_price !== undefined) fields.invoicePrice.value = data.unit_price;
        status.textContent = 'AI suggestion loaded. Confirm every field before checking.';
        updatePreview();
      } catch (error) {
        status.textContent = 'AI extraction unavailable. Please use the manual fields.';
      } finally {
        button.disabled = false;
      }
    });
  }

  updatePreview();
})();
