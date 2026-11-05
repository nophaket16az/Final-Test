# Automated Testing: Selenium / Robot Framework / Playwright / Cypress

ตัวอย่างการเขียน **automated test** ด้วยเครื่องมือ 4 ตัว ทุกตัวทดสอบเว็บเดียวกันด้วย test case ชุดเดียวกัน จะได้เทียบกันได้ และ**รันได้จริงทันที** เพราะมีเว็บตัวอย่าง (`demo-app/`) อยู่ในเครื่อง ไม่ต้องพึ่งอินเทอร์เน็ต

| เครื่องมือ | ภาษา | ไฟล์ทดสอบ |
|---|---|---|
| Selenium + pytest | Python | `selenium/test_login.py`, `selenium/test_register.py` |
| Robot Framework + SeleniumLibrary | Robot (Keyword) | `robot/login.robot`, `robot/register.robot` |
| Playwright + pytest | Python | `playwright/test_login.py`, `playwright/test_register.py` |
| Cypress | JavaScript | `cypress/e2e/login.cy.js`, `cypress/e2e/register.cy.js` |

---

## สารบัญ
1. [เว็บที่ใช้ทดสอบ](#1-เว็บที่ใช้ทดสอบ-demo-app)
2. [Test cases](#2-test-cases)
3. [โครงสร้างโปรเจกต์](#3-โครงสร้างโปรเจกต์)
4. [ติดตั้ง](#4-ติดตั้ง)
5. [วิธีรัน](#5-วิธีรัน)
6. [วิธีปรับแก้ไปใช้กับเว็บอื่น](#6-วิธีปรับแก้ไปใช้กับเว็บอื่น-สำคัญตอนสอบ)
7. [ตัวอย่าง Google ของอาจารย์](#7-ตัวอย่างค้นหา-google-จากสไลด์)
8. [เปรียบเทียบ 4 เครื่องมือ](#8-เปรียบเทียบ-4-เครื่องมือ)
9. [หลักฐานที่ต้องเก็บใส่ Word](#9-หลักฐานที่ต้องเก็บใส่-word)
10. [ปัญหาที่เจอบ่อย](#10-ปัญหาที่เจอบ่อย)

---

## 1. เว็บที่ใช้ทดสอบ (demo-app)

เว็บร้านค้าจำลอง 3 หน้า เลียนแบบเว็บฝึกเทสต์ [saucedemo.com](https://www.saucedemo.com) (ใช้ id ของช่องกรอกแบบเดียวกัน)

| หน้า | สิ่งที่มี |
|---|---|
| `index.html` | หน้า Login (`#user-name`, `#password`, `#login-button`, ข้อความ error `[data-test="error"]`) |
| `inventory.html` | หน้าสินค้า หัวข้อ `.title` = "Products", ปุ่ม `#add-to-cart-sauce-labs-backpack`, ตัวเลขตะกร้า `.shopping_cart_badge` |
| `register.html` | ช่องกรอกอายุ `#age` (กฎ: 18-60), ปุ่ม `#submit`, ผลลัพธ์ `#result` |

ผู้ใช้ที่ login ได้: **`standard_user`** / **`secret_sauce`** (ส่วน `locked_out_user` จะถูกล็อก)

---

## 2. Test cases

ทุกเครื่องมือมี test case ชุดเดียวกัน **17 เคส**

### Login (6 เคส)
| # | Input | ผลที่คาดหวัง |
|---|---|---|
| TC01 | `standard_user` / `secret_sauce` | เข้าหน้า **Products** |
| TC02 | login แล้วกด Add to cart | ตะกร้าแสดง **1** |
| TC03 | รหัสผิด | `Username and password do not match` |
| TC04 | ไม่กรอก username | `Username is required` |
| TC05 | ไม่กรอก password | `Password is required` |
| TC06 | `locked_out_user` | `locked out` |

### Register: ช่องอายุ 18-60 (11 เคส) ใช้เทคนิค Black box จากบทที่ 12
| เทคนิค | ค่าที่ทดสอบ | ผลที่คาดหวัง |
|---|---|---|
| EP (Equivalence Partitioning) | 10 / **35** / 70 | ไม่ผ่าน / **ผ่าน** / ไม่ผ่าน |
| BVA (Boundary Value Analysis) | 17 / **18** / **19** / **59** / **60** / 61 | 17 กับ 61 ไม่ผ่าน ที่เหลือผ่าน |
| Error guessing | ช่องว่าง, `abc` | `Age is required`, `Age must be a number` |

---

## 3. โครงสร้างโปรเจกต์

```
automate-test/
├── README.md
├── requirements.txt          # แพ็กเกจ Python
├── package.json              # โปรเจกต์ Node.js (Cypress)
├── cypress.config.js         # ตั้งค่า Cypress (baseUrl)
├── demo-app/                 # เว็บที่ใช้ทดสอบ
│   ├── index.html
│   ├── inventory.html
│   ├── register.html
│   └── style.css
├── selenium/
│   ├── conftest.py           # เปิด/ปิด Chrome ให้ทุก test
│   ├── test_login.py
│   └── test_register.py
├── robot/
│   ├── login.robot
│   └── register.robot
├── playwright/
│   ├── conftest.py
│   ├── test_login.py
│   └── test_register.py
├── cypress/e2e/
│   ├── login.cy.js
│   ├── register.cy.js
│   └── google/google_search.cy.js
└── google-examples/          # ตัวอย่างค้นหา Google จากสไลด์
    ├── selenium_google.py
    ├── google_search.robot
    └── playwright_google.py
```

---

## 4. ติดตั้ง

ต้องมี **Python 3.9+**, **Node.js (LTS)** และ **Google Chrome** ก่อน
(Windows: ตอนติดตั้ง Python ให้ติ๊ก **Add Python to PATH**)

```bash
python --version
node -v
npm -v
```

### 4.1 ฝั่ง Python (Selenium, Robot Framework, Playwright) ด้วย uv

```bash
# เข้าโฟลเดอร์โปรเจกต์
cd automate-test

# 1. ติดตั้ง uv
pip install uv

# 2. สร้าง venv
uv venv

# 3. เปิดใช้งาน venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 4. ติดตั้งแพ็กเกจ (ตามอาจารย์ + pytest สำหรับรันเทสต์)
uv pip install selenium playwright robotframework robotframework-seleniumlibrary pytest pytest-playwright
#   หรือ  uv pip install -r requirements.txt

# 5. ดาวน์โหลดเบราว์เซอร์ของ Playwright (ขาดขั้นนี้ Playwright รันไม่ได้)
playwright install chromium
```

ตรวจสอบ:
```bash
uv --version
uv pip list
robot --version
playwright --version
```

> Selenium 4.6+ มี Selenium Manager หา ChromeDriver ให้อัตโนมัติ ไม่ต้องดาวน์โหลด driver เอง

### 4.2 ฝั่ง Node.js (Cypress)

```bash
npm install cypress --save-dev
npx cypress --version
npx cypress verify
```

> repo นี้มี `package.json` อยู่แล้ว เลยไม่ต้อง `npm init -y` ถ้าเริ่มโปรเจกต์ใหม่เองค่อยรัน `npm init -y` ก่อน

---

## 5. วิธีรัน

### ขั้นที่ 0: เปิดเว็บ demo-app ก่อนทุกครั้ง (เปิด terminal ทิ้งไว้ 1 หน้าต่าง)

```bash
python -m http.server 8000 --directory demo-app
```

เปิด http://localhost:8000 ในเบราว์เซอร์ ต้องเห็นหน้า Login แล้ว**เปิด terminal ใหม่**สำหรับรันเทสต์ (อย่าลืมเปิด venv ในหน้าต่างใหม่ด้วย)

### 5.1 Selenium

```bash
cd selenium
pytest -v
```

- จะเห็น Chrome เปิดขึ้นมาทำทีละเคส จบแล้ว terminal แสดง **`17 passed`**
- รันแบบไม่เปิดหน้าต่าง: `HEADLESS=1 pytest -v` (Windows PowerShell: `$env:HEADLESS="1"; pytest -v`)
- รันเฉพาะไฟล์: `pytest test_login.py -v` / เฉพาะเคส: `pytest -k success -v`

**อธิบายโค้ด**
- `conftest.py` มี fixture `driver` เปิด Chrome ก่อนแต่ละ test แล้ว `quit()` หลังจบ
- `login()` คือฟังก์ชันที่ใช้ซ้ำ: `driver.get()` เปิดหน้า → `find_element(By.ID, ...)` หาช่อง → `send_keys()` พิมพ์ → `click()`
- `assert ... == "Products"` คือตรวจผล ถ้าไม่ตรง test จะ FAIL
- `@pytest.mark.parametrize` คือ data-driven: ฟังก์ชันเดียวรันหลายชุดข้อมูล

### 5.2 Robot Framework

```bash
robot --outputdir results robot/
```

- terminal แสดงทีละเคสว่า **PASS / FAIL** สรุป `17 tests, 17 passed`
- เปิดผลลัพธ์ `results/report.html` และ `results/log.html` (log มีทุกขั้นตอนพร้อม screenshot ตอน fail)
- รันแบบไม่เปิดหน้าต่าง: `robot --outputdir results -v BROWSER:headlesschrome robot/`
- รันเฉพาะไฟล์: `robot --outputdir results robot/login.robot`

**อธิบายโค้ด**
- `*** Settings ***` เรียก `SeleniumLibrary`, `Suite Setup` เปิดเบราว์เซอร์ครั้งเดียวก่อนเริ่ม, `Suite Teardown` ปิดตอนจบ
- `*** Variables ***` เก็บค่า `${URL}`, `${BROWSER}`, `${USERNAME}`
- `*** Keywords ***` สร้าง keyword เอง เช่น `Login` รับ `[Arguments]`
- `[Template]` / `Test Template` คือ data-driven: 1 แถว = 1 test case (ดูใน `register.robot`)
- keyword ตรวจผล: `Element Text Should Be` (ตรงทั้งหมด), `Element Should Contain` (มีคำนี้)

### 5.3 Playwright

```bash
cd playwright
pytest -v --headed
```

- `--headed` = เปิดหน้าต่างให้เห็น (ไม่ใส่ = headless เร็วกว่า)
- ให้ทำช้าลงจะได้ดูทัน: `pytest -v --headed --slowmo 500`
- อัดการกระทำบนเว็บเป็นโค้ดอัตโนมัติ: `playwright codegen http://localhost:8000`

**อธิบายโค้ด**
- `page` มาจาก pytest-playwright เปิด/ปิดเบราว์เซอร์ให้เอง
- `page.fill("#user-name", ...)` กรอก, `page.click(...)` คลิก (รอ element พร้อมให้เองอัตโนมัติ)
- `expect(page.locator(".title")).to_have_text("Products")` คือตรวจผล (รอจนกว่าจะตรง หรือ timeout)

### 5.4 Cypress

```bash
npx cypress open
```
1. เลือก **E2E Testing** → เลือกเบราว์เซอร์ → **Start E2E Testing**
2. คลิก `login.cy.js` หรือ `register.cy.js` จะเห็นแต่ละเคสขึ้นเครื่องหมายถูกสีเขียว

รันแบบ headless ใน terminal: `npm run cy:run`

**อธิบายโค้ด**
- `cypress.config.js` ตั้ง `baseUrl` ไว้ `cy.visit('/')` จึงเปิด http://localhost:8000
- `describe` / `it` จัดกลุ่มและตั้งชื่อ test
- `cy.get('#user-name').type(...)` กรอก, `.click()` คลิก
- `.should('have.text', 'Products')` / `.should('contain', ...)` คือตรวจผล
- `failCases.forEach(...)` คือ data-driven แบบ JavaScript

---

## 6. วิธีปรับแก้ไปใช้กับเว็บอื่น (สำคัญตอนสอบ)

ทุกเทสต์มี 3 ส่วนที่ต้องแก้ ตามลำดับนี้

### 6.1 เปลี่ยน URL

| เครื่องมือ | แก้ตรงไหน | หรือส่งตอนรัน |
|---|---|---|
| Selenium / Playwright | `BASE_URL` ใน `conftest.py` | `BASE_URL=https://example.com pytest -v` |
| Robot | `${URL}` ใน `*** Variables ***` | `robot -v URL:https://example.com robot/` |
| Cypress | `baseUrl` ใน `cypress.config.js` | `npx cypress run --config baseUrl=https://example.com` |

> Windows PowerShell ตั้งตัวแปรแบบนี้: `$env:BASE_URL="https://example.com"; pytest -v`

### 6.2 เปลี่ยน locator (บอกว่าจะหา element ไหน)

เปิดเว็บ → คลิกขวาที่ช่อง/ปุ่ม → **Inspect** → ดู `id`, `name`, `class` หรือ `data-test`

| HTML ที่เห็น | Selenium | Robot | Playwright / Cypress |
|---|---|---|---|
| `<input id="email">` | `By.ID, "email"` | `id:email` | `"#email"` |
| `<input name="q">` | `By.NAME, "q"` | `name:q` | `"[name='q']"` |
| `<span class="title">` | `By.CSS_SELECTOR, ".title"` | `css:.title` | `".title"` |
| `<button data-test="login">` | `By.CSS_SELECTOR, "[data-test='login']"` | `css:[data-test="login"]` | `"[data-test='login']"` |
| ปุ่มที่มีคำว่า Login | `By.XPATH, "//button[text()='Login']"` | `xpath://button[text()="Login"]` | `"text=Login"` (Playwright) / `cy.contains('Login')` |

> ทางลัด: `playwright codegen https://เว็บที่จะเทสต์` แล้วกดใช้งานเว็บ Playwright จะเขียนโค้ดพร้อม locator ให้ ก๊อปไปใช้ได้เลย

### 6.3 เปลี่ยนข้อมูลทดสอบ / เพิ่ม test case

- **Selenium / Playwright**: เพิ่มแถวใน `@pytest.mark.parametrize([...])`
- **Robot**: เพิ่มแถวใต้ `*** Test Cases ***` ใน `register.robot` (1 แถว = 1 เคส) หรือเพิ่มเคสใหม่ที่เรียก keyword `Login`
- **Cypress**: เพิ่มแถวใน array `failCases` / `cases`

ตัวอย่างเพิ่มเคส "อายุ 0" ทั้ง 4 ตัว:
```python
("0", "Age must be between 18 and 60"),               # Selenium / Playwright
```
```robot
Age Zero              0          ${INVALID}            # Robot
```
```js
['0', INVALID],                                       // Cypress
```

### 6.4 ตัวอย่าง: เปลี่ยนไปเทสต์ saucedemo.com ของจริง

demo-app ใช้ id เดียวกับ https://www.saucedemo.com เทสต์ Login จึงน่าจะรันกับเว็บจริงได้โดยแก้แค่ URL (ยังไม่ได้ลองกับเว็บจริงจากเครื่องที่ทำ repo นี้ ถ้าเทสต์ไหนไม่ผ่านให้ตรวจ locator ตามข้อ 6.2)

```bash
BASE_URL=https://www.saucedemo.com pytest test_login.py -v           # ในโฟลเดอร์ selenium หรือ playwright
robot -v URL:https://www.saucedemo.com --outputdir results robot/login.robot
npx cypress run --config baseUrl=https://www.saucedemo.com --spec cypress/e2e/login.cy.js
```
(`register` มีเฉพาะใน demo-app saucedemo ไม่มีหน้านี้)

### 6.5 คำสั่งที่ใช้บ่อย (cheat sheet)

| ทำอะไร | Selenium | Robot | Playwright | Cypress |
|---|---|---|---|---|
| เปิดหน้า | `driver.get(url)` | `Go To  url` | `page.goto(url)` | `cy.visit(url)` |
| กรอก | `.send_keys("x")` | `Input Text  loc  x` | `page.fill(loc, "x")` | `cy.get(loc).type('x')` |
| คลิก | `.click()` | `Click Button  loc` / `Click Element  loc` | `page.click(loc)` | `cy.get(loc).click()` |
| กด Enter | `Keys.RETURN` | `Press Keys  loc  RETURN` | `page.keyboard.press("Enter")` | `.type('x{enter}')` |
| เลือก dropdown | `Select(el).select_by_value("v")` | `Select From List By Value  loc  v` | `page.select_option(loc, "v")` | `cy.get(loc).select('v')` |
| ตรวจข้อความตรง | `assert el.text == "x"` | `Element Text Should Be  loc  x` | `expect(loc).to_have_text("x")` | `.should('have.text','x')` |
| ตรวจมีคำนี้ | `assert "x" in el.text` | `Element Should Contain  loc  x` | `expect(loc).to_contain_text("x")` | `.should('contain','x')` |
| ตรวจหน้าเว็บมีคำ | `assert "x" in driver.page_source` | `Page Should Contain  x` | `expect(page.locator("body")).to_contain_text("x")` | `cy.contains('x')` |
| ตรวจ URL | `assert "x" in driver.current_url` | `Location Should Contain  x` | `expect(page).to_have_url(re.compile("x"))` | `cy.url().should('include','x')` |

---

## 7. ตัวอย่างค้นหา Google (จากสไลด์)

ตัวอย่างของอาจารย์ แก้ตัวอักษรเพี้ยน (`&quot;`, `&#39;`) ที่ติดมาตอนคัดลอกแล้ว

```bash
python google-examples/selenium_google.py
robot --outputdir results google-examples/google_search.robot
python google-examples/playwright_google.py
npx cypress open        # แล้วเลือก google/google_search.cy.js
```

> Google อาจขึ้น CAPTCHA หรือหน้ายอมรับคุกกี้เมื่อรู้ว่าเป็นบอท ทำให้เทสต์ค้าง ถ้าเจอให้กดผ่านเอง ตัวอย่างนี้จึงเหมาะกับการเก็บหลักฐานติดตั้ง ส่วนการฝึกเขียนเทสต์ให้ใช้ demo-app

---

## 8. เปรียบเทียบ 4 เครื่องมือ

| | Selenium | Robot Framework | Playwright | Cypress |
|---|---|---|---|---|
| ภาษา | Python, Java, JS, C# ฯลฯ | Keyword (ต่อยอดด้วย Python/Java) | Python, JS/TS, Java, .NET | JavaScript / TypeScript |
| จุดเด่น | มาตรฐานเก่าแก่ หลายภาษา หลายเบราว์เซอร์ | อ่านง่ายเหมือนภาษาคน มี report/log ในตัว | เร็ว, รอ element ให้เอง (auto-wait), codegen | all-in-one, เห็นการรันแบบ real-time, debug ง่าย |
| ข้อจำกัด | ต้องจัดการการรอ (wait) เอง | ต้องพึ่ง library เช่น SeleniumLibrary | ใหม่กว่า ตัวอย่างน้อยกว่า Selenium | JS อย่างเดียว เน้นเว็บ |
| ตรวจผลด้วย | `assert` (pytest) | keyword `Should Be` / `Should Contain` | `expect(...)` | `.should(...)` |

---

## 9. หลักฐานที่ต้องเก็บใส่ Word

แคปหน้าจอให้เห็นทั้ง**คำสั่ง**และ**ผลลัพธ์**

- [ ] **Python**: `python --version`
- [ ] **uv**: `uv --version`, `uv venv`, `uv pip install ...` สำเร็จ
- [ ] **Node.js**: `node -v`, `npm -v`
- [ ] **Selenium**: `uv pip list` เห็น selenium + ผล `pytest -v` (17 passed) หรือ Chrome ที่ค้น Google
- [ ] **Robot Framework**: `robot --version` + ผลรัน PASS + หน้า `report.html`
- [ ] **Playwright**: `playwright --version` + ผล `pytest -v --headed`
- [ ] **Cypress**: `npx cypress --version` + หน้าต่าง Cypress ที่ทุกเคสเป็นสีเขียว

---

## 10. ปัญหาที่เจอบ่อย

| อาการ | วิธีแก้ |
|---|---|
| `'python' is not recognized` | ติดตั้ง Python ใหม่แล้วติ๊ก Add to PATH หรือใช้ `py` แทน `python` |
| `robot` / `pytest` / `playwright` : command not found | ยังไม่ได้เปิด venv (`.venv\Scripts\activate`) หรือใช้ `uv run` นำหน้า เช่น `uv run pytest -v` |
| PowerShell ไม่ยอมรัน `activate` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` แล้วลองใหม่ |
| เทสต์ fail ทุกเคส / `ERR_CONNECTION_REFUSED` | ลืมเปิดเว็บ demo-app (ขั้นที่ 0) |
| Playwright: `Executable doesn't exist` | รัน `playwright install chromium` |
| `pytest` หา `conftest` ผิดตัว | ให้ `cd` เข้าโฟลเดอร์ `selenium` หรือ `playwright` ก่อนรัน (อย่ารันสองโฟลเดอร์พร้อมกัน) |
| Selenium/Robot บน Linux, Docker หรือ Jenkins ขึ้น `Chrome instance exited` | Selenium: `NO_SANDBOX=1 HEADLESS=1 pytest -v` / Robot: `robot -v BROWSER:headlesschrome -v 'OPTIONS:add_argument("--no-sandbox")' robot/` |
| เทสต์ fail เพราะหา element ไม่เจอ | locator ผิด ให้ Inspect ใหม่ (ข้อ 6.2) หรือหน้าเว็บโหลดช้า |
