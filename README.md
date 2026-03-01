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

### Development

```bash
# optional: load environment variables from a .env file
# (requires python-dotenv which is included in requirements)
python -m flask run --app app.py --debug
```

এইভাবে চালালে ডিবাগ মোডে কাজ করবে এবং আপনি কোড পরিবর্তন করলে সার্ভার
রিলোড হবে। ডিফল্ট ইউআরএল http://127.0.0.1:5000 অথবা http://localhost:5000

### Production

প্রোডাকশনে সরাসরি `python app.py` ব্যবহার না করে WSGI সার্ভার ব্যবহার
করুন। লিনাক্স/ইউনিক্স পরিবেশে `gunicorn` সাধারণ পছন্দ:

```bash
# ধরুন পরিবেশে PORT সেট আছে (Heroku-style)
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

উইন্ডোজে `gunicorn` মূলত সমর্থিত নয়, সেখানে `waitress` বা `uwsgi`
যেমন উইন্ডোজ‑অনুকূল সার্ভার দেখুন:

```bash
pip install waitress
python -m waitress --port=$PORT app:app
```

`-w 4` ইত্যাদি বিকল্পগুলো ব্যবহার করে worker সংখ্যা বাড়াতে পারেন।

অন্যদিকে, পাইথনের জন্য `uwsgi`, `hypercorn`, `uvicorn` ইত্যাদি
ওই পরিবেশগুলিতে ব্যবহার করা যায়।

### পরিবেশ ভেরিয়েবল

- `WKHTMLTOPDF_PATH`: wkhtmltopdf বাইনারির ফাইলপথ (প্রক্সি না দিলে
default ব্যবহার হবে)
- `PORT`: ওয়েবসার্ভার শোনার পোর্ট
- `FLASK_DEBUG`: ডিবাগ মোড চালু করতে "1" অথবা "true"

`.env` ফাইল তৈরি করলে সেটিংগুলো অটোমেটিক লোড হবে (ব্যবহার করে
`python-dotenv`)।

### স্ট্যাটিক ফাইল সার্ভিং

এই অ্যাপ মূলত ডাইনামিক পিডিএফ তৈরি করে; স্ট্যাটিক ফাইলগুলো (সিল,
সই) Flask নিজেই সার্ভ করবে, তবে বড় প্রোডাকশনে এগুলো CDN বা NGINX এর
পেছনে রাখা উত্তম।

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
