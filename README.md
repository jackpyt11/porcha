# খতিয়ান পর্চা পিডিএফ জেনারেটর

Flask ভিত্তিক অ্যাপ — HTML টেম্পলেট থেকে ডাইনামিক খতিয়ান পর্চা পিডিএফ তৈরি।

## সেটআপ

1. **ভার্চুয়াল এনভায়রনমেন্ট (ঐচ্ছিক)**  
   `python -m venv venv` তারপর `venv\Scripts\activate`

2. **প্যাকেজ ইন্সটল**  
   `pip install -r requirements.txt`

3. **wkhtmltopdf ইন্সটল** (অবশ্যক)  
   - ডাউনলোড: https://wkhtmltopdf.org/downloads.html  
   - Windows এ ডিফল্ট পাথ: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`  
   - অন্য পাথে ইন্সটল করলে এনভায়রনমেন্ট ভেরিয়েবল সেট করুন:  
     `set WKHTMLTOPDF_PATH=C:\YourPath\wkhtmltopdf.exe`

4. **সিল ও সই**  
   - সিল: `static/seals/official_seal.png` (Transparent PNG)  
   - সই: `static/signatures/officer_sig.png` (Transparent PNG)

## চালানোর নিয়ম

```bash
python app.py
```

ব্রাউজারে যান: http://127.0.0.1:5000  
ফরম পূরণ করে "পিডিএফ তৈরি করুন" ক্লিক করলে পিডিএফ ডাউনলোড হবে।

**কোনো তথ্য সংরক্ষণ হয় না** — ফরমের ডাটা বা পিডিএফ সার্ভারে সেভ হয় না, শুধু ডাউনলোড দেয়।

## প্রোজেক্ট স্ট্রাকচার

```
├── app.py              # মেইন Flask অ্যাপ
├── templates/
│   ├── form.html       # ইনপুট ফরম
│   └── index.html      # পর্চা ডকুমেন্ট টেম্পলেট (পিডিএফে রূপান্তর হয়)
├── static/
│   ├── seals/          # সিলের ছবি
│   └── signatures/     # সই এর ছবি
└── requirements.txt
```
# porcha
