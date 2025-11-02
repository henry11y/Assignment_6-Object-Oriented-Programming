# Build Customer objects from LoansDataset.csv (no pandas/csv)

DATA_PATH = r"C:\Users\henry\OneDrive\INFO INFRAS\built in functions\LoansDataset.csv"

class Customer:
    def __init__(self, customer_id, name, loan_amount, interest_rate, term_months, status):
        self.customer_id = str(customer_id).strip()
        self.name = str(name).strip()
        self.loan_amount = float(str(loan_amount).replace("£", "").replace(",", "").strip() or 0)
        self.interest_rate = float(str(interest_rate).replace("%", "").strip() or 0)
        self.term_months = int(float(str(term_months).strip() or 0))
        self.status = str(status).strip()

    def __str__(self):
        return (f"Customer ID: {self.customer_id} | Name: {self.name} | "
                f"Loan: ${self.loan_amount:,.2f} | Interest: {self.interest_rate:.2f}% | "
                f"Term: {self.term_months} months | Status: {self.status}")

def split_csv_line(line):
    # simple comma-split that respects quotes
    parts = []
    buf = []
    in_quotes = False
    for ch in line:
        if ch == '"':
            in_quotes = not in_quotes
            continue
        if ch == ',' and not in_quotes:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf).strip())
    return parts

def load_customers(file_path):
    customers = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return customers

    if not lines:
        print("File is empty.")
        return customers

    # read header and build index map
    header = split_csv_line(lines[0])
    h = [h.lower() for h in header]

    def ix(name):
        try:
            return h.index(name)
        except ValueError:
            return -1

    id_i    = ix("customer_id")
    amt_i   = ix("loan_amnt")
    rate_i  = ix("loan_int_rate")
    term_i  = ix("term_years")
    stat_i  = ix("current_loan_status")

    if min(id_i, amt_i, rate_i, term_i, stat_i) < 0:
        print("Required columns not found in header.")
        return customers

    parsed = skipped = 0
    for line in lines[1:]:
        cols = split_csv_line(line)
        # guard for short rows
        if len(cols) <= max(id_i, amt_i, rate_i, term_i, stat_i):
            skipped += 1
            continue
        try:
            cid = cols[id_i]
            name = f"Customer {cid}"               # dataset has no name field
            amount = cols[amt_i]                   # like "£35,000.00"
            rate = cols[rate_i]                    # like 16.02
            term_months = float(cols[term_i]) * 12 # years -> months
            status = cols[stat_i]

            cust = Customer(cid, name, amount, rate, term_months, status)
            customers.append(cust)
            parsed += 1
        except Exception:
            skipped += 1
            continue

    for c in customers:
        print(c)
    print(f"Parsed: {parsed} | Skipped: {skipped} | Total customers: {len(customers)}")
    return customers

if __name__ == "__main__":
    print(f"Reading: {DATA_PATH}")
    load_customers(DATA_PATH)
