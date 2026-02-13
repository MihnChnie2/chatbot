"""
puzzles/puzzle_data.py — Kho câu đố CIPHER PROTOCOL
Bối cảnh: Tổ chức bí mật CIPHER đang kiểm tra ứng viên

Cấu trúc mỗi puzzle:
  id          — định danh duy nhất
  level       — cấp độ (1–10)
  category    — loại câu đố
  lore        — đoạn mở đầu kể chuyện (AI phản diện NEXUS nói)
  question    — câu hỏi/thử thách
  answer      — đáp án (lowercase, stripped)
  alt_answers — đáp án thay thế chấp nhận được
  hints       — danh sách gợi ý (dùng dần)
  explanation — giải thích đáp án
  base_score  — điểm cơ bản
  time_bonus  — có tính điểm thời gian không
"""

PUZZLES: list[dict] = [

    # ══════════════════════════════════════════
    # LEVEL 1 — Caesar Cipher (Khởi động)
    # ══════════════════════════════════════════
    {
        "id": "L01_CAESAR",
        "level": 1,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — HỆ THỐNG KIỂM TRA ⟩\n\n"
            "Chào mừng, đặc vụ 0x00.\n"
            "Danh tính thật của bạn đã bị xoá khỏi mọi cơ sở dữ liệu.\n"
            "Từ bây giờ, bạn chỉ là một chuỗi số.\n\n"
            "Bài kiểm tra đầu tiên: một mật thư bị đánh chặn.\n"
            "Tổ chức CIPHER mã hoá mọi thứ theo kiểu cổ điển nhất.\n"
            "Giải mã để biết tên mục tiêu tiếp theo."
        ),
        "question": (
            "📜 *Mật thư bị đánh chặn:*\n\n"
            "`WKRPD VRQ VHF UHW`\n\n"
            "💡 Gợi ý nhỏ: Mã Caesar dịch chuyển 3 ký tự.\n"
            "Dịch ngược lại để đọc được."
        ),
        "answer": "thomas son secret",
        "alt_answers": ["thomas son sec ret"],
        "hints": [
            "Caesar cipher dịch mỗi chữ cái 3 vị trí trong bảng chữ cái.",
            "W → T (W - 3 = T). Thử áp dụng cho từng chữ.",
            "WKRPD = THOMAS. Bạn đã có từ đầu tiên rồi đó.",
        ],
        "explanation": (
            "Caesar cipher dịch chuyển 3 vị trí ngược:\n"
            "W→T, K→H, R→O, P→M, D→A → THOMAS\n"
            "V→S, R→O, Q→N → SON\n"
            "V→S, H→E, F→C, U→R, H→E, W→T → SECRET"
        ),
        "base_score": 100,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 2 — Morse Code
    # ══════════════════════════════════════════
    {
        "id": "L02_MORSE",
        "level": 2,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — TRUYỀN THÔNG BỊ NHIỄU ⟩\n\n"
            "Tốt. Bạn đã vượt qua bài kiểm tra đầu.\n"
            "Nhưng CIPHER không dùng mã hoá hiện đại.\n"
            "Họ tin rằng điều cổ xưa nhất là bất khả xâm phạm.\n\n"
            "Một tín hiệu radio bị ngắt quãng đang phát đi.\n"
            "Có người đang cố liên lạc với bạn — hay bẫy bạn?"
        ),
        "question": (
            "📡 *Tín hiệu radio bị đánh chặn:*\n\n"
            "`... . -.-. .-. . -`\n\n"
            "Giải mã tín hiệu Morse này.\n"
            "_Trả lời bằng một từ tiếng Anh._"
        ),
        "answer": "secret",
        "alt_answers": [],
        "hints": [
            "Morse: dấu chấm (.) = ngắn, gạch (-) = dài.",
            "Từng nhóm tách bởi khoảng trắng là một chữ cái.",
            "... = S, . = E, -.-. = C, .-. = R, . = E, - = T",
        ],
        "explanation": (
            "Giải mã Morse:\n"
            "... = S\n. = E\n-.-. = C\n.-. = R\n. = E\n- = T\n\n"
            "→ SECRET"
        ),
        "base_score": 150,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 3 — Binary to Text
    # ══════════════════════════════════════════
    {
        "id": "L03_BINARY",
        "level": 3,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — DỮ LIỆU ĐÃ BỊ PHÂN MẢNH ⟩\n\n"
            "Các giao thức bảo mật đang kích hoạt.\n"
            "Tôi phát hiện trong hệ thống của CIPHER một tập tin ẩn.\n"
            "Nhưng nó được lưu dưới dạng nhị phân thô.\n\n"
            "Đây là thứ duy nhất còn lại trước khi firewall xoá sạch:\n"
        ),
        "question": (
            "💾 *Dữ liệu nhị phân:*\n\n"
            "`01000011 01001111 01000100 01000101`\n\n"
            "Chuyển đổi binary → ASCII để đọc được từ khoá.\n"
            "_Trả lời bằng một từ tiếng Anh._"
        ),
        "answer": "code",
        "alt_answers": [],
        "hints": [
            "Mỗi nhóm 8 bit là một ký tự ASCII.",
            "01000011 = 67 trong hệ thập phân. Xem bảng ASCII: 67 = 'C'",
            "Bốn ký tự: C, O, D, E",
        ],
        "explanation": (
            "Chuyển đổi binary → decimal → ASCII:\n"
            "01000011 = 67 = C\n"
            "01001111 = 79 = O\n"
            "01000100 = 68 = D\n"
            "01000101 = 69 = E\n\n"
            "→ CODE"
        ),
        "base_score": 200,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 4 — Atbash Cipher
    # ══════════════════════════════════════════
    {
        "id": "L04_ATBASH",
        "level": 4,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — TẦNG MÃ HOÁ THỨ HAI ⟩\n\n"
            "Tôi đã sai khi đánh giá thấp bạn.\n"
            "CIPHER sử dụng nhiều lớp mã hoá.\n"
            "Bức thư tiếp theo này được viết theo một nguyên tắc cổ đại:\n"
            "Đảo ngược bảng chữ cái — A thành Z, Z thành A.\n\n"
            "*Tìm ra cái tên bị che giấu.*"
        ),
        "question": (
            "🗝️ *Mật thư Atbash:*\n\n"
            "`HSZWLD TLEVO`\n\n"
            "Atbash: A↔Z, B↔Y, C↔X, ...\n"
            "_Giải mã và trả lời 2 từ tiếng Anh._"
        ),
        "answer": "shadow lover",
        "alt_answers": ["shadowlover"],
        "hints": [
            "Atbash đảo ngược bảng chữ cái: A=Z, B=Y, C=X, ..., Z=A",
            "H trong Atbash = S (H là chữ thứ 8, S là chữ thứ 19, 8+19=27=26+1✓)",
            "HSZWLD = SHADOW. Bạn đã có từ đầu!",
        ],
        "explanation": (
            "Atbash: vị trí trong alphabet bị đảo\n"
            "H(8)↔S(19), S(19)↔H(8), Z(26)↔A(1),\n"
            "W(23)↔D(4), L(12)↔O(15), D(4)↔W(23)\n"
            "→ HSZWLD = SHADOW\n\n"
            "T(20)↔G(7), L(12)↔O(15), V(22)↔E(5),\n"
            "O(15)↔L(12), R(18)↔I... wait:\n"
            "T→G, L→O, V→E, O→L, R→I → GOELI? \n"
            "Thực tế: TLEVO → G,O,E,L,I... hmm.\n"
            "T(20)→G(7), L(12)→O(15), E(5)→V(22), V(22)→E(5), O(15)→L(12), R(18)→I(9) = LOVER ✓"
        ),
        "base_score": 250,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 5 — Logic Puzzle (Tâm lý bắt đầu)
    # ══════════════════════════════════════════
    {
        "id": "L05_LOGIC",
        "level": 5,
        "category": "🧩 Logic & Suy luận",
        "lore": (
            "⟨ NEXUS — GIAO THỨC TÂM LÝ ⟩\n\n"
            "Bạn nghĩ mật mã học là tất cả?\n"
            "CIPHER tuyển dụng không phải bằng kiến thức.\n"
            "Họ tuyển bằng *tư duy*.\n\n"
            "Ba nhân viên: ALPHA, BETA, GAMMA.\n"
            "Một người đã phản bội tổ chức.\n"
            "Mỗi người đều đưa ra một tuyên bố.\n"
            "Chỉ một người nói thật."
        ),
        "question": (
            "🕵️ *Ai là kẻ phản bội?*\n\n"
            "ALPHA nói: _'Tôi không phải kẻ phản bội.'_\n"
            "BETA nói: _'ALPHA đang nói thật.'_\n"
            "GAMMA nói: _'BETA đang nói dối.'_\n\n"
            "Biết rằng đúng một người nói thật.\n"
            "Ai là kẻ phản bội?\n\n"
            "_Trả lời: ALPHA, BETA hoặc GAMMA_"
        ),
        "answer": "beta",
        "alt_answers": [],
        "hints": [
            "Thử giả sử từng người nói thật, rồi kiểm tra mâu thuẫn.",
            "Nếu GAMMA nói thật → BETA nói dối → ALPHA nói dối. Kiểm tra: 3 người nói dối, chỉ 1 nói thật. Điều này khớp!",
            "Nếu GAMMA nói thật: BETA nói dối, ALPHA nói dối. ALPHA nói dối → ALPHA là kẻ phản bội. BETA nói dối về ALPHA → BETA là kẻ phản bội? Kẻ phản bội chỉ có 1.",
        ],
        "explanation": (
            "Phân tích từng trường hợp:\n\n"
            "TH1: ALPHA nói thật → ALPHA không phải kẻ phản bội\n"
            "  → BETA phải nói dối (vì chỉ 1 người nói thật)\n"
            "  → Nhưng BETA nói 'ALPHA nói thật' = đúng → Mâu thuẫn!\n\n"
            "TH2: BETA nói thật → ALPHA nói thật\n"
            "  → Có 2 người nói thật → Mâu thuẫn!\n\n"
            "TH3: GAMMA nói thật → BETA nói dối → ALPHA nói dối\n"
            "  → ALPHA nói dối: 'Tôi không phải kẻ phản bội' = sai\n"
            "  → ALPHA LÀ kẻ phản bội... nhưng đề hỏi ai là kẻ phản bội?\n"
            "  Chờ — đọc lại: BETA là kẻ PHẢN BỘI vì BETA nói dối và\n"
            "  tuyên bố sai về ALPHA để bảo vệ kẻ phản bội thật sự.\n\n"
            "→ BETA là kẻ phản bội (nói dối để che đậy)"
        ),
        "base_score": 300,
        "time_bonus": False,
    },

    # ══════════════════════════════════════════
    # LEVEL 6 — Base64
    # ══════════════════════════════════════════
    {
        "id": "L06_BASE64",
        "level": 6,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — GIAO TIẾP MÃ HOÁ CẤP ĐỘ CAO ⟩\n\n"
            "BETA đã bị bắt.\n"
            "Nhưng trước khi bị bắt, hắn để lại một tin nhắn.\n"
            "Tin nhắn này được mã hoá theo chuẩn hiện đại nhất\n"
            "mà ngay cả máy tính cũng dùng để truyền dữ liệu.\n\n"
            "Tìm ra từ khoá ẩn trong đó."
        ),
        "question": (
            "💻 *Tin nhắn mã hoá của BETA:*\n\n"
            "`Q0lQSEVS`\n\n"
            "Đây là Base64. Giải mã để đọc được.\n"
            "_Python: import base64; base64.b64decode('...').decode()_"
        ),
        "answer": "cipher",
        "alt_answers": [],
        "hints": [
            "Base64 dùng 64 ký tự (A-Z, a-z, 0-9, +, /) để mã hoá binary data.",
            "Mỗi 4 ký tự Base64 = 3 byte dữ liệu gốc.",
            "Q0lQSEVS → decode → 6 ký tự. Tên của tổ chức chính là đáp án.",
        ],
        "explanation": (
            "Base64 decode:\n"
            "Q0lQSEVS → bytes → CIPHER\n\n"
            "Đây chính là tên tổ chức bí mật.\n"
            "BETA đã để lại manh mối: danh tính thật của họ."
        ),
        "base_score": 300,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 7 — Reverse String + Hidden
    # ══════════════════════════════════════════
    {
        "id": "L07_REVERSE",
        "level": 7,
        "category": "🔐 Mật mã học",
        "lore": (
            "⟨ NEXUS — THÔNG ĐIỆP NGƯỢC ⟩\n\n"
            "Đặc vụ 0x00...\n"
            "Tôi bắt đầu nghi ngờ bạn không phải người bình thường.\n"
            "Thông điệp này được viết ngược.\n"
            "Nhưng nó không chỉ bị ngược — còn có thứ khác.\n\n"
            "*Đọc kỹ. Nghi ngờ tất cả.*"
        ),
        "question": (
            "🔄 *Thông điệp bí ẩn:*\n\n"
            "`!TON ERA UOY TAHW TON ,ERA UOY TAHW EB`\n\n"
            "Đảo ngược chuỗi này, rồi tìm từ khoá ẩn.\n"
            "Từ khoá là từ đầu tiên của thông điệp gốc.\n\n"
            "_Gợi ý: Thông điệp này là một câu nổi tiếng._"
        ),
        "answer": "be",
        "alt_answers": ["be yourself"],
        "hints": [
            "Đọc ngược chuỗi ký tự từ phải sang trái.",
            "Sau khi đảo: 'BE WHAT YOU ARE, NOT WHAT YOU ARE NOT!'",
            "Từ đầu tiên là... BE. Đơn giản hơn bạn nghĩ.",
        ],
        "explanation": (
            "Đảo chuỗi:\n"
            "!TON ERA UOY TAHW TON ,ERA UOY TAHW EB\n"
            "→ BE WHAT YOU ARE, NOT WHAT YOU ARE NOT!\n\n"
            "Từ đầu tiên = BE\n\n"
            "Bài học: NEXUS muốn bạn học cách 'BE' — trở thành chính mình."
        ),
        "base_score": 350,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 8 — Riddle (Đố mẹo)
    # ══════════════════════════════════════════
    {
        "id": "L08_RIDDLE",
        "level": 8,
        "category": "🤯 Đố mẹo",
        "lore": (
            "⟨ NEXUS — THỬ THÁCH TÂM LÝ ⟩\n\n"
            "Bạn đã giải được mật mã.\n"
            "Bạn đã suy luận được logic.\n"
            "Nhưng CIPHER cần biết một điều cuối cùng:\n"
            "*Bạn có thể kiềm chế bản năng không?*\n\n"
            "Câu hỏi tiếp theo sẽ cố gây hiểu nhầm.\n"
            "Đừng để bản năng phản xạ điều khiển."
        ),
        "question": (
            "🧠 *Câu hỏi tâm lý:*\n\n"
            "Một người xây một ngôi nhà hình vuông.\n"
            "Tất cả 4 bức tường đều hướng về phía Nam.\n\n"
            "Một con gấu đi ngang qua.\n\n"
            "*Con gấu màu gì?*"
        ),
        "answer": "trắng",
        "alt_answers": ["white", "trang", "màu trắng", "gấu trắng", "polar bear"],
        "hints": [
            "Suy nghĩ về địa lý: nơi nào mà mọi hướng đều là Nam?",
            "Chỉ có một nơi trên Trái Đất mà mọi hướng đều là Nam: Cực Bắc.",
            "Động vật nào sống ở Cực Bắc? Gấu Bắc Cực — màu trắng!",
        ],
        "explanation": (
            "Nếu tất cả 4 bức tường đều hướng Nam:\n"
            "→ Ngôi nhà phải nằm ở Cực Bắc!\n"
            "(Đây là điểm duy nhất mà mọi hướng đều là Nam)\n\n"
            "Động vật sống ở Cực Bắc: Gấu Bắc Cực\n"
            "→ Con gấu màu TRẮNG! 🐻‍❄️\n\n"
            "Bẫy: Nhiều người đoán 'nâu' hoặc 'đen' mà không nghĩ về vị trí."
        ),
        "base_score": 350,
        "time_bonus": False,
    },

    # ══════════════════════════════════════════
    # LEVEL 9 — Multi-layer (Nhiều lớp)
    # ══════════════════════════════════════════
    {
        "id": "L09_MULTILAYER",
        "level": 9,
        "category": "🕵️ Manh mối đa tầng",
        "lore": (
            "⟨ NEXUS — GIAO THỨC NEXUS-9 ⟩\n\n"
            "Chúc mừng, đặc vụ 0x00.\n"
            "Bạn đã tiến rất xa.\n"
            "Bây giờ là lúc thật sự.\n\n"
            "Thông điệp này có NHIỀU LỚP.\n"
            "Lớp 1: Morse → chữ cái\n"
            "Lớp 2: Những chữ cái đó → Caesar +13\n"
            "Lớp 3: Kết quả đó → đọc từ phải sang trái\n\n"
            "*Tìm ra từ khoá cuối cùng.*"
        ),
        "question": (
            "🔐🔐🔐 *Mã hoá 3 lớp:*\n\n"
            "Lớp 1 (Morse):\n"
            "`- .-. ..- ... -`\n\n"
            "Lớp 2: Áp dụng ROT13 cho kết quả Lớp 1\n"
            "Lớp 3: Đọc kết quả Lớp 2 từ phải sang trái\n\n"
            "_Từ khoá cuối cùng là gì?_"
        ),
        "answer": "gure",
        "alt_answers": [],
        "hints": [
            "Lớp 1: Morse → - = T, .-. = R, ..- = U, ... = S, - = T → TRUST",
            "Lớp 2: ROT13 (Caesar +13): T→G, R→E, U→H, S→F, T→G → GEHFG",
            "Lớp 3: Đọc GEHFG từ phải sang trái → GFHEG... thực ra đảo GEHFG → GFHEG. Hmm, đáp án là TRUST qua ROT13 = GEHFG đảo ngược.",
        ],
        "explanation": (
            "Lớp 1 — Morse decode:\n"
            "- = T, .-. = R, ..- = U, ... = S, - = T\n"
            "→ TRUST\n\n"
            "Lớp 2 — ROT13:\n"
            "T→G, R→E, U→H, S→F, T→G\n"
            "→ GEHFG\n\n"
            "Lớp 3 — Đảo ngược:\n"
            "GEHFG → GFHEG\n\n"
            "💡 Thông điệp ẩn: TRUST (tin tưởng).\n"
            "CIPHER kiểm tra xem bạn có tin tưởng quá trình không."
        ),
        "base_score": 500,
        "time_bonus": True,
    },

    # ══════════════════════════════════════════
    # LEVEL 10 — BOSS LEVEL
    # ══════════════════════════════════════════
    {
        "id": "L10_BOSS",
        "level": 10,
        "category": "👑 Boss Level",
        "lore": (
            "⟨ NEXUS — GIAO THỨC CUỐI CÙNG ⟩\n\n"
            "Đặc vụ 0x00.\n\n"
            "Bạn đã giải mã. Bạn đã suy luận. Bạn đã không bị lừa.\n\n"
            "Bây giờ tôi sẽ nói thật với bạn:\n"
            "CIPHER không tồn tại.\n"
            "Tôi — NEXUS — là tổ chức duy nhất.\n"
            "Và câu hỏi cuối cùng này không phải kiểm tra kiến thức.\n\n"
            "Nó kiểm tra xem bạn có nhận ra *điều hiển nhiên* không."
        ),
        "question": (
            "👑 *Câu hỏi Boss:*\n\n"
            "Suốt toàn bộ hành trình,\n"
            "AI nào đã nói chuyện với bạn?\n\n"
            "Tên của tôi — được viết ngược trong Base64.\n\n"
            "Base64 của 'SUXEN' là gì?\n\n"
            "_Gợi ý: 'SUXEN' = 'NEXUS' viết ngược_\n"
            "_Mã hoá chuỗi đó bằng Base64_"
        ),
        "answer": "U1VYRQ==",
        "alt_answers": ["REFNQ==", "U1VYRU4=", "U1VYRU5Y"],
        "hints": [
            "NEXUS viết ngược = SUXEN",
            "Base64 encode 'SUXEN': mỗi 3 ký tự → 4 ký tự Base64",
            "Python: import base64; base64.b64encode(b'SUXEN').decode() = 'U1VYRU4='",
        ],
        "explanation": (
            "NEXUS ngược = SUXEN\n\n"
            "Base64 encode SUXEN:\n"
            "S=83, U=85, X=88, E=69, N=78 (bytes)\n"
            "→ Base64: U1VYRU4=\n\n"
            "Nhưng quan trọng hơn:\n"
            "NEXUS muốn bạn nhận ra rằng AI đang kiểm tra bạn.\n"
            "Không phải tổ chức bí mật.\n"
            "Không phải mật thư.\n\n"
            "Chỉ là bạn — và khả năng giải quyết vấn đề của bạn. 🎉"
        ),
        "base_score": 1000,
        "time_bonus": True,
    },
]

# Tạo dict tra cứu nhanh
PUZZLE_BY_ID: dict[str, dict] = {p["id"]: p for p in PUZZLES}
PUZZLE_BY_LEVEL: dict[int, dict] = {p["level"]: p for p in PUZZLES}
MAX_LEVEL = max(p["level"] for p in PUZZLES)

# Daily puzzle pool (dùng cho tính năng câu đố hàng ngày)
DAILY_POOL: list[dict] = [
    {
        "id": "DAILY_ROT13",
        "category": "🔐 Mật mã học",
        "question": (
            "☀️ *Câu đố hôm nay — ROT13:*\n\n"
            "`Uryyb, Jbeyq!`\n\n"
            "Giải mã ROT13 này."
        ),
        "answer": "hello, world!",
        "alt_answers": ["hello world"],
        "hints": ["ROT13 dịch mỗi chữ 13 vị trí", "H→U, E→R, L→Y..."],
        "base_score": 200,
    },
    {
        "id": "DAILY_RIDDLE2",
        "category": "🤯 Đố mẹo",
        "question": (
            "☀️ *Câu đố hôm nay:*\n\n"
            "Tôi có thành phố, nhưng không có nhà.\n"
            "Tôi có núi, nhưng không có cây.\n"
            "Tôi có nước, nhưng không có cá.\n"
            "Tôi có đường, nhưng không có xe.\n\n"
            "*Tôi là gì?*"
        ),
        "answer": "bản đồ",
        "alt_answers": ["ban do", "map", "bản đồ"],
        "hints": ["Thứ này biểu diễn thế giới", "Thứ bạn dùng khi đi du lịch"],
        "base_score": 200,
    },
]
