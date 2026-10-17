"""Reproducible synthetic English SMS dataset (Indian scam scenarios). Fictional orgs, reserved example URLs."""
import random, csv
SEED, VERSION = 42, "synthetic-v1"
R = random.Random(SEED)
BANKS = ["Northstar Bank","Bharat Union Bank","Lotus Savings Bank","Riverdale Bank","Apex Co-op Bank","Metro Trust Bank"]
COUR = ["SwiftPost","QuickParcel","Demo Logistics","Roadrunner Couriers","ParcelNest"]
APPS = ["PayEasy","QuickPay","UPIGo","PaySwift"]
NAMES = ["Ravi","Anita","Suresh","Priya","Kiran","Meena","Arjun","Divya"]
def url(): return R.choice(["http://example.com/","https://example.org/","http://secure-update.example.net/"])+R.choice(["verify","k1","p","claim","login","track"])+str(R.randint(10,9999))
def amt(): return R.choice(["Rs.","INR ","Rs "])+f"{R.choice([199,499,750,1250,2500,4999,9800,15000,50000,250000]):,}"
T = [
("scam","bank_phishing",[
 "Dear customer, your {b} account {a} will be blocked today. Update your details now: {u}",
 "ALERT: Unusual login on your {b} netbanking. Confirm identity immediately or account gets suspended {u}",
 "{b}: Your debit card is deactivated. Call 9{p} and share card number to reactivate.",
 "Your {b} account has been temporarily restricted. Click {u} to restore access within 24 hrs",
 "Security notice from {b}. Verify your PAN to avoid freezing of account {a}. {u}"]),
("scam","upi_fraud",[
 "You have received a collect request of {m} on {ap}. Enter your UPI PIN to receive money.",
 "Refund of {m} pending. Scan the QR sent to you and enter PIN to accept refund. {u}",
 "{ap} cashback {m} credited soon. Approve the request on your app and enter PIN to claim.",
 "Wrong transfer of {m} made to your number. Please return it urgently to 9{p}@upi, I am in trouble."]),
("scam","kyc_scam",[
 "Your {b} KYC has expired. Update now or account will be closed today. {u}",
 "Dear user, KYC verification pending. Submit Aadhaar and PAN at {u} to avoid deactivation.",
 "{ap} wallet KYC incomplete! Limit blocked. Complete e-KYC in 2 hours: {u}",
 "KYC update required. Download the support app from {u} and share the code shown."]),
("scam","otp_theft",[
 "I sent my OTP to your number by mistake. Please forward the code {o} to me urgently.",
 "{b} support: To cancel the pending transaction of {m}, share the OTP you just received.",
 "Congrats! Reward points redeemed. Reply with the 6 digit code received to confirm {o}",
 "Your account will be locked unless you read out the verification code to our executive calling now."]),
("scam","courier_fee",[
 "{c}: Your parcel is held at hub. Pay customs fee of {m} at {u} to release delivery.",
 "Package undeliverable due to incomplete address. Update address and pay Rs 25 re-delivery fee: {u}",
 "{c} notice: Shipment {t} on hold. Pay {m} handling charge today or it will be returned. {u}"]),
("scam","lottery_prize",[
 "Congratulations {n}! You won {m} in the Mega Lucky Draw. Claim now at {u}",
 "WINNER! Your mobile number selected for a free gift voucher worth {m}. Pay processing fee to receive.",
 "You are our lucky customer. Win a new smartphone! Click {u} before midnight to claim prize."]),
("scam","fake_job",[
 "Work from home, earn {m} per day! Just like and review videos. Join on WhatsApp 9{p} now.",
 "Hiring part time data entry. Salary {m}/week. Pay registration fee of Rs 999 to confirm your seat. {u}",
 "Dear candidate, you are shortlisted for an MNC job. Deposit {m} as security to receive offer letter."]),
("scam","loan_offer",[
 "Pre-approved instant loan of {m} with no documents! Pay Rs 1,500 processing fee to release. {u}",
 "Urgent loan approved for {n}. Zero CIBIL check. Send processing charges to receive amount today.",
 "Get {m} loan in 5 minutes. Install app from {u} and allow access to contacts and gallery."]),
("scam","bill_disconnection",[
 "Your electricity connection will be disconnected tonight at 9:30 PM due to unpaid bill. Call officer 9{p} immediately.",
 "Power supply to be cut today. Previous month bill not updated. Pay via {u} to avoid disconnection.",
 "Gas service will be stopped. Update bill details now at {u} and call 9{p}."]),
("scam","investment",[
 "Join our VIP stock tips group. Guaranteed 300% returns in 7 days. Invest {m} today: {u}",
 "Crypto doubling scheme! Invest {m} and get double in 24 hours. Limited slots. {u}",
 "Insider trading calls by SEBI registered analyst. Pay {m} for guaranteed profit {u}"]),
("scam","urgent_payment",[
 "Hi, this is {n}, I lost my phone and need {m} urgently. Please send to this number via {ap}, will return tonight.",
 "Boss here. I am in a meeting, need gift cards worth {m} right away. Reply quickly, confidential.",
 "Your relative has met with an accident. Send {m} to this account immediately for surgery 9{p}."]),
("legitimate","bank_txn",[
 "{b}: Rs {x} debited from A/c {a} on {d}. Avl bal Rs {y}. Not you? Call the number on your card.",
 "Your A/c {a} is credited with {m} on {d}. Ref no {t}. - {b}",
 "{b}: Your monthly statement for A/c {a} is ready. View it in the official mobile app.",
 "UPI txn of {m} to {n} successful. UPI Ref {t}. - {b}"]),
("legitimate","otp_legit",[
 "{o} is your one time password for login. Valid for 10 minutes. Do not share it with anyone. - {b}",
 "Use {o} to verify your sign in to {ap}. Never share this code, our staff will never ask for it.",
 "Your OTP for the transaction of {m} is {o}. It expires in 5 mins. If not done by you, call us."]),
("legitimate","delivery_update",[
 "{c}: Your order {t} is out for delivery today. Delivery partner will call you before arrival.",
 "Your parcel {t} has been delivered at {tm}. Thanks for shopping with us.",
 "Order {t} shipped. Expected delivery by {d}. Track in the app."]),
("legitimate","bill_payment",[
 "Payment of {m} received for your electricity bill. Receipt no {t}. Thank you.",
 "Your broadband bill of {m} is due on {d}. Pay through the official app to avoid late fee.",
 "Recharge of {m} successful for your mobile. Validity 28 days."]),
("legitimate","appointment",[
 "Reminder: appointment with Dr. {n} on {d} at {tm}. Reply C to confirm or R to reschedule.",
 "Your dental check up is scheduled for tomorrow at {tm}. Please carry previous reports.",
 "Hi {n}, your vehicle service is booked for {d}. See you at the workshop."]),
("legitimate","job_ack",[
 "Thank you for applying to the Associate role. Your application ref {t} is received. We will contact shortlisted candidates.",
 "Your interview is scheduled on {d} at {tm} via the video link emailed to you. Best wishes - HR team.",
 "Application update: your profile is under review. No fee is charged at any stage of hiring."]),
("legitimate","personal",[
 "Hey {n}, running 10 mins late. Start without me.",
 "Can you pick up milk on your way home? Also call mom at {tm}.",
 "Happy birthday {n}! Dinner at 8 tomorrow, don't be late.",
 "Meeting moved to {tm}. Bring the printed notes please.",
 "Did you see the match last night? Unbelievable ending!"]),
("legitimate","service_notice",[
 "{b} will undergo scheduled maintenance on {d} from 1 AM to 3 AM. Services may be unavailable.",
 "Your complaint {t} has been resolved. Rate our support in the official app.",
 "Dear customer, your policy renewal is due on {d}. Visit our branch or official website to renew."])]
def fill(t):
    return t.format(b=R.choice(BANKS),c=R.choice(COUR),ap=R.choice(APPS),n=R.choice(NAMES),u=url(),m=amt(),
      a="XX"+str(R.randint(1000,9999)),o=str(R.randint(100000,999999)),t=f"{R.choice('ABCXYZ')}{R.randint(10000000,99999999)}",
      tm=f"{R.randint(1,12)}:{R.randint(10,59)} {R.choice(['AM','PM'])}",p=R.randint(100000000,999999999),
      x=f"{R.randint(50,9999)}.{R.randint(10,99)}",y=f"{R.randint(500,99999)}.{R.randint(10,99)}",
      d=f"{R.randint(1,28)}-{R.choice(['Jan','Feb','Mar','Apr','Jun','Aug','Oct','Dec'])}-2026")
def mutate(s):
    if R.random()<.03: s=s.upper()
    if R.random()<.2: s=s.replace("Dear customer, ","")
    if R.random()<.15: s=s+R.choice([" Thanks."," Please act."," Regards."])
    return s.strip()
def main(n=60, out="ml/data/sms_dataset.csv"):
    rows, seen, i = [], set(), 0
    for label, st, tpls in T:
        for ti, tpl in enumerate(tpls):
            for _ in range(n):
                txt = mutate(fill(tpl))
                if txt in seen: continue
                seen.add(txt); i += 1
                rows.append(dict(message_id=f"syn-{i:05d}",text=txt,label=label,scam_type=st if label=="scam" else "none",
                  source_type="synthetic",source_reference=f"{VERSION};seed={SEED};family={st}-{ti}",review_status="unreviewed",
                  explanation=("Matches "+st.replace('_',' ')+" pattern (pressure, payment or credential request)") if label=="scam" else "Routine informational message with no request for secrets or payment to unknown parties"))
    R.shuffle(rows)
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {out}")
if __name__=="__main__": main()
