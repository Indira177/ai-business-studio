let allInvoices = [];

// ==========================================
// NAVIGATION
// ==========================================

function setActiveNav(page) {
    document.querySelectorAll(".sidebar-nav .nav-item").forEach(function (item) {
        item.classList.remove("active");

        const href = item.getAttribute("href");

        if (
            (page === "dashboard" && href === "#dashboard") ||
            (page === "invoices" && href === "#invoices") ||
            (page === "website-builder" && href === "#website-builder")
        ) {
            item.classList.add("active");
        }
    });
}

function hideAllSections() {
    const dashboard = document.getElementById("dashboardSection");
    const websiteBuilder = document.getElementById("websiteBuilderSection");
    const generatedWebsites = document.getElementById("generatedWebsitesSection");

    if (dashboard) dashboard.style.display = "none";
    if (websiteBuilder) websiteBuilder.style.display = "none";
    if (generatedWebsites) generatedWebsites.style.display = "none";
}

function showDashboard() {
    hideAllSections();

    const dashboard = document.getElementById("dashboardSection");
    if (dashboard) dashboard.style.display = "block";

    setActiveNav("dashboard");
    loadInvoices();
    loadWebsites();
}

function showInvoices() {
    hideAllSections();

    // The invoice panel is inside dashboardSection in index.html.
    const dashboard = document.getElementById("dashboardSection");
    const invoicePanel = document.getElementById("invoicePanel");

    if (dashboard) dashboard.style.display = "block";

    if (invoicePanel) {
        invoicePanel.style.display = "block";
        invoicePanel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    setActiveNav("invoices");
    loadInvoices();
}

function showWebsiteBuilder() {
    hideAllSections();

    const builder = document.getElementById("websiteBuilderSection");
    const websites = document.getElementById("generatedWebsitesSection");

    if (builder) builder.style.display = "block";
    if (websites) websites.style.display = "block";

    setActiveNav("website-builder");
    loadWebsites();
}

// ==========================================
// INVOICES
// ==========================================

async function loadInvoices() {
    const table = document.getElementById("invoiceTable");
    const totalInvoices = document.getElementById("totalInvoices");
    const totalAmount = document.getElementById("totalAmount");

    if (!table) return;

    table.innerHTML = '<tr><td colspan="6">Loading invoices...</td></tr>';

    try {
        const response = await fetch("/api/invoices");

        if (!response.ok) {
            throw new Error("Invoice API returned HTTP " + response.status);
        }

        const result = await response.json();
        const receivedInvoices = Array.isArray(result.data) ? result.data : [];

        // Ignore empty/malformed rows and prevent identical invoices appearing twice.
        const seenInvoices = new Set();
        allInvoices = receivedInvoices.filter(function (invoice) {
            if (!invoice || typeof invoice !== "object") return false;

            const hasUsefulData = [
                invoice.invoice_number,
                invoice.vendor_name,
                invoice.customer_name,
                invoice.invoice_date,
                invoice.total_amount
            ].some(function (value) {
                return value !== null && value !== undefined && String(value).trim() !== "";
            });
            if (!hasUsefulData) return false;

            const key = [
                invoice.invoice_number || "",
                invoice.vendor_name || "",
                invoice.customer_name || "",
                invoice.invoice_date || "",
                invoice.total_amount ?? ""
            ].map(function (value) {
                return String(value).trim().toLowerCase();
            }).join("|");

            if (seenInvoices.has(key)) return false;
            seenInvoices.add(key);
            return true;
        });

        if (totalInvoices) totalInvoices.textContent = allInvoices.length;

        const amount = allInvoices.reduce(function (sum, invoice) {
            const value = Number(invoice.total_amount);
            return sum + (Number.isFinite(value) ? value : 0);
        }, 0);

        if (totalAmount) totalAmount.textContent = "$" + amount.toFixed(2);

        displayInvoices(allInvoices);
    } catch (error) {
        console.error("LOAD INVOICES ERROR:", error);

        if (totalInvoices) totalInvoices.textContent = "0";
        if (totalAmount) totalAmount.textContent = "$0.00";

        table.innerHTML =
            '<tr><td colspan="6">Unable to load invoices. Please refresh and try again.</td></tr>';
    }
}

function displayInvoices(invoices) {
    const table = document.getElementById("invoiceTable");
    if (!table) return;

    if (!invoices.length) {
        table.innerHTML = '<tr><td colspan="6">No invoices found.</td></tr>';
        return;
    }

    table.innerHTML = invoices.map(function (invoice) {
        const id = Number(invoice.invoice_id);

        return `
            <tr>
                <td><strong>#${escapeHtml(invoice.invoice_number || "N/A")}</strong></td>
                <td>${escapeHtml(invoice.vendor_name || "N/A")}</td>
                <td>${escapeHtml(invoice.customer_name || "N/A")}</td>
                <td>${escapeHtml(invoice.invoice_date || "N/A")}</td>
                <td><strong>${formatMoney(invoice.total_amount)}</strong></td>
                <td>
                    <button class="view-button" onclick="viewInvoice(${id})">
                        View
                    </button>
                </td>
            </tr>
        `;
    }).join("");
}

function filterInvoices() {
    const input = document.getElementById("invoiceSearch");
    if (!input) return;

    const query = input.value.toLowerCase().trim();

    displayInvoices(allInvoices.filter(function (invoice) {
        return [
            invoice.invoice_number,
            invoice.vendor_name,
            invoice.customer_name,
            invoice.invoice_date
        ].some(function (value) {
            return String(value || "").toLowerCase().includes(query);
        });
    }));
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatMoney(value) {
    const amount = Number(value);
    return value !== null && value !== "" && Number.isFinite(amount)
        ? "$" + amount.toFixed(2)
        : "N/A";
}

// ==========================================
// INVOICE DETAILS
// ==========================================

async function viewInvoice(invoiceId) {
    try {
        const response = await fetch("/api/invoices/" + encodeURIComponent(invoiceId));

        if (!response.ok) {
            throw new Error("Invoice details returned HTTP " + response.status);
        }

        const result = await response.json();
        const invoice = result.data;

        if (!invoice) throw new Error("Invoice details were not returned.");

        setText("detailInvoiceNumber", invoice.invoice_number);
        setText("detailVendor", invoice.vendor_name);
        setText("detailCustomer", invoice.customer_name);
        setText("detailDate", invoice.invoice_date);
        setText("detailDueDate", invoice.due_date);
        setText("detailGST", invoice.gst_number);
        setText("detailSubtotal", formatMoney(invoice.subtotal));
        setText("detailTax", formatMoney(invoice.tax_amount));
        setText("detailTotal", formatMoney(invoice.total_amount));

        const modal = document.getElementById("invoiceModal");
        if (modal) modal.style.display = "flex";
    } catch (error) {
        console.error("VIEW INVOICE ERROR:", error);
        alert("Unable to load invoice details.");
    }
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent =
            value !== null && value !== undefined && value !== ""
                ? value
                : "N/A";
    }
}

function closeInvoiceDetails() {
    const modal = document.getElementById("invoiceModal");
    if (modal) modal.style.display = "none";
}

// ==========================================
// UPLOAD INVOICE
// ==========================================

function openUpload() {
    const modal = document.getElementById("uploadModal");
    const status = document.getElementById("uploadStatus");

    if (modal) modal.style.display = "flex";
    if (status) status.textContent = "";
}

function closeUpload() {
    const modal = document.getElementById("uploadModal");
    if (modal) modal.style.display = "none";
}

async function uploadInvoice() {
    const fileInput = document.getElementById("invoiceFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput || !status) return;

    if (!fileInput.files || !fileInput.files.length) {
        status.textContent = "Please select a PDF invoice.";
        return;
    }

    const file = fileInput.files[0];

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Only PDF files are supported.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    status.textContent = "Analyzing invoice...";

    try {
        const response = await fetch("/api/invoices/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof result.detail === "string"
                    ? result.detail
                    : "Invoice upload returned HTTP " + response.status
            );
        }

        status.textContent = "Invoice analyzed successfully!";
        await loadInvoices();

        setTimeout(function () {
            closeUpload();
            fileInput.value = "";
            status.textContent = "";
        }, 1000);
    } catch (error) {
        console.error("UPLOAD INVOICE ERROR:", error);
        status.textContent = "Error: " + error.message;
    }
}

// ==========================================
// WEBSITES
// ==========================================

async function loadWebsites() {
    try {
        const response = await fetch("/api/websites");
        if (!response.ok) throw new Error("HTTP " + response.status);

        const result = await response.json();
        const websites = Array.isArray(result.data) ? result.data : [];

        const count = document.getElementById("totalWebsites");
        if (count) {
            count.textContent = typeof result.count === "number"
                ? result.count
                : websites.length;
        }

        const list = document.getElementById("websiteList");
        if (!list) return;

        if (!websites.length) {
            list.innerHTML =
                '<div class="website-list-empty">No websites have been generated yet.</div>';
            return;
        }

        list.innerHTML = websites.map(function (website) {
            const id = Number(website.website_id);
            const name = escapeHtml(website.business_name || "Business Website");
            const description = escapeHtml(website.description || "Generated business website");
            const style = escapeHtml(website.style || "Modern");
            const created = website.created_at
                ? new Date(website.created_at).toLocaleDateString()
                : "Recently";

            return `
                <div class="website-item">
                    <div class="website-item-icon">🌐</div>
                    <h3>${name}</h3>
                    <p class="website-item-description">${description}</p>
                    <div class="website-item-meta">
                        <span class="website-meta-badge">${style}</span>
                        <span class="website-meta-badge">Created ${escapeHtml(created)}</span>
                        <span class="website-meta-badge">ID #${id}</span>
                    </div>
                    <div class="website-item-actions">
                        <a href="/api/websites/${id}/preview" target="_blank" rel="noopener"
                           class="website-list-preview">👁 Preview</a>
                        <a href="/api/websites/${id}/download"
                           class="website-list-download">⬇ Download</a>
                        <button type="button" class="website-list-delete"
                                onclick="deleteWebsite(${id})">🗑 Delete</button>
                    </div>
                </div>
            `;
        }).join("");
    } catch (error) {
        console.error("LOAD WEBSITES ERROR:", error);

        const list = document.getElementById("websiteList");
        if (list) {
            list.innerHTML =
                '<div class="website-list-empty">Unable to load generated websites.</div>';
        }
    }
}

async function deleteWebsite(websiteId) {
    if (!confirm("Are you sure you want to delete this website?")) return;

    try {
        const response = await fetch("/api/websites/" + websiteId, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof result.detail === "string"
                    ? result.detail
                    : "Delete failed: HTTP " + response.status
            );
        }

        alert("Website deleted successfully.");
        await loadWebsites();
    } catch (error) {
        console.error("DELETE WEBSITE ERROR:", error);
        alert("Unable to delete website: " + error.message);
    }
}

// ==========================================
// INITIALIZE AND BROWSER NAVIGATION
// ==========================================

document.addEventListener("DOMContentLoaded", function () {
    const invoiceModal = document.getElementById("invoiceModal");
    const uploadModal = document.getElementById("uploadModal");
    const searchBox = document.getElementById("invoiceSearch");

    if (invoiceModal) {
        invoiceModal.addEventListener("click", function (event) {
            if (event.target === invoiceModal) closeInvoiceDetails();
        });
    }

    if (uploadModal) {
        uploadModal.addEventListener("click", function (event) {
            if (event.target === uploadModal) closeUpload();
        });
    }

    if (searchBox) {
        searchBox.addEventListener("input", filterInvoices);
    }

    if (window.location.hash === "#website-builder") {
        showWebsiteBuilder();
    } else if (window.location.hash === "#invoices") {
        showInvoices();
    } else {
        showDashboard();
    }
});

window.addEventListener("hashchange", function () {
    if (window.location.hash === "#website-builder") {
        showWebsiteBuilder();
    } else if (window.location.hash === "#invoices") {
        showInvoices();
    } else {
        showDashboard();
    }
});
