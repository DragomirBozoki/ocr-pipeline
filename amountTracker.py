class AmountTracker:
    def __init__(self, tolerance=2, min_change=0.01):
        self.max_amount = 0.0
        self.tolerance = tolerance  # koliko loših frameova možemo ignorisati
        self.bad_frame_count = 0
        self.last_valid = None
        self.min_change = min_change  # najmanja očekivana promena (kao 1 cent)

    def is_valid_step(self, prev, curr):
        """Da li je promena između dva broja logična (samo neka cifra se promenila)?"""
        if abs(curr - prev) < self.min_change:
            return False
        prev_str = f"{int(prev):,}"
        curr_str = f"{int(curr):,}"
        diffs = sum(a != b for a, b in zip(prev_str[::-1], curr_str[::-1]))
        return diffs <= 2  # najviše 2 različite cifre — inače previše skače

    def update(self, detected_amounts):
        """Vrati najverovatniji novi iznos ili None ako je nevalidno."""
        for amount_str in detected_amounts:
            try:
                amount_val = float(amount_str.replace("€", "").replace(",", ""))
            except:
                continue

            if amount_val >= self.max_amount:
                if self.last_valid is None or self.is_valid_step(self.last_valid, amount_val):
                    self.max_amount = amount_val
                    self.bad_frame_count = 0
                    self.last_valid = amount_val
                    return f"€{amount_val:,.2f}"
                else:
                    self.bad_frame_count += 1
            else:
                # manji je od trenutnog maksimuma
                self.bad_frame_count += 1

            if self.bad_frame_count > self.tolerance:
                print("⚠️  Too many bad frames — waiting for new stable value.")
        return None
