from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters,
)

# =========================
# 1. THONG TIN BOT
# =========================
BOT_TOKEN = "8700458186:AAGkBmnGhb4_yWdyMoCV4q-BwH_1FBP8kf4"
BOT_USERNAME = "wellcome_gold_bot"  # khong co @

# =========================
# 2. NOI DUNG WELCOME
# =========================
WELCOME_TEXT = (
    "👋 Chào mừng bạn đến với Thị Trường Vàng Việt!\n\n"
    "Chọn mục phù hợp bên dưới để bắt đầu:"
)

# =========================
# 3. TAO LINK CHAT RIENG CHO TUNG MUC
# =========================
def build_private_link(payload: str) -> str:
    return f"https://t.me/{BOT_USERNAME}?start={payload}"

# =========================
# 4. MENU CHINH TRONG GROUP
# =========================
def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("📈 Nhận tín hiệu miễn phí", url=build_private_link("free_signal"))],
        [InlineKeyboardButton("💎 Vào Nhóm V.I.P", url=build_private_link("vip_group"))],
        [InlineKeyboardButton("🧭 Chọn lộ trình phù hợp", url=build_private_link("roadmap"))],
        [InlineKeyboardButton("☎️ Liên hệ admin", url=build_private_link("contact_admin"))],
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# 5. MENU CON TRONG CHAT RIENG
# =========================
def build_free_signal_menu():
    keyboard = [
        [InlineKeyboardButton("📌 Cách đọc tín hiệu", callback_data="free_read_signal")],
        [InlineKeyboardButton("🕒 Khung giờ trade đẹp", callback_data="free_trade_time")],
        [InlineKeyboardButton("🛡 Quản lý vốn cơ bản", callback_data="free_risk")],
        [InlineKeyboardButton("☎️ Liên hệ admin hỗ trợ", url=build_private_link("contact_admin"))],
        [InlineKeyboardButton("⬅️ Quay lại menu chính", callback_data="back_private_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_vip_menu():
    keyboard = [
        [InlineKeyboardButton("💎 Quyền lợi nhóm V.I.P", callback_data="vip_benefits")],
        [InlineKeyboardButton("🎯 Ai phù hợp với V.I.P", callback_data="vip_fit")],
        [InlineKeyboardButton("📩 Cách tham gia", callback_data="vip_join")],
        [InlineKeyboardButton("☎️ Liên hệ admin hỗ trợ", url=build_private_link("contact_admin"))],
        [InlineKeyboardButton("⬅️ Quay lại menu chính", callback_data="back_private_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_roadmap_menu():
    keyboard = [
        [InlineKeyboardButton("🌱 Tôi là người mới tập trade vàng", callback_data="roadmap_newbie")],
        [InlineKeyboardButton("🔥 Tôi đã có kinh nghiệm trade vàng", callback_data="roadmap_experienced")],
        [InlineKeyboardButton("⬅️ Quay lại menu chính", callback_data="back_private_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_newbie_menu():
    keyboard = [
        [InlineKeyboardButton("📘 Bắt đầu từ đâu", callback_data="newbie_start")],
        [InlineKeyboardButton("💰 Quản lý vốn cơ bản", callback_data="newbie_risk")],
        [InlineKeyboardButton("⛔ Những lỗi người mới hay mắc", callback_data="newbie_mistakes")],
        [InlineKeyboardButton("☎️ Liên hệ admin hỗ trợ", url=build_private_link("contact_admin"))],
        [InlineKeyboardButton("⬅️ Quay lại lộ trình", callback_data="back_roadmap")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_experienced_menu():
    keyboard = [
        [InlineKeyboardButton("🎯 Tối ưu điểm vào lệnh", callback_data="exp_entry")],
        [InlineKeyboardButton("📊 Lọc tín hiệu chất lượng", callback_data="exp_filter_signal")],
        [InlineKeyboardButton("⚙️ Quản lý vốn nâng cao", callback_data="exp_risk")],
        [InlineKeyboardButton("☎️ Liên hệ admin hỗ trợ", url=build_private_link("contact_admin"))],
        [InlineKeyboardButton("⬅️ Quay lại lộ trình", callback_data="back_roadmap")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_contact_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Nhắn admin ngay", url="https://t.me/ryantranec")],
        [InlineKeyboardButton("💎 Hỏi về nhóm V.I.P", callback_data="contact_vip")],
        [InlineKeyboardButton("📈 Hỏi về tín hiệu", callback_data="contact_signal")],
        [InlineKeyboardButton("⬅️ Quay lại menu chính", callback_data="back_private_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_private_main_menu():
    keyboard = [
        [InlineKeyboardButton("📈 Nhận tín hiệu miễn phí", callback_data="private_main_free")],
        [InlineKeyboardButton("💎 Vào Nhóm V.I.P", callback_data="private_main_vip")],
        [InlineKeyboardButton("🧭 Chọn lộ trình phù hợp", callback_data="private_main_roadmap")],
        [InlineKeyboardButton("☎️ Liên hệ admin", callback_data="private_main_contact")],
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# 6. KHI CO THANH VIEN MOI VAO GROUP
# =========================
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message:
        return

    if not message.new_chat_members:
        return
    
    print("=== NEW_CHAT_MEMBERS EVENT ===")
    print("Chat ID:", update.effective_chat.id)
    print("Chat title:", update.effective_chat.title)
    print("Members joined:", [m.full_name for m in message.new_chat_members])

    for member in message.new_chat_members:
        if member.id == context.bot.id:
            continue

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{WELCOME_TEXT}\n\n🎯 Chào mừng {member.full_name}",
            reply_markup=build_main_menu()
        )

# =========================
# 7. LENH /start TRONG CHAT RIENG
# =========================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # start payload từ deep link
    payload = ""
    if context.args:
        payload = context.args[0]

    # Nếu user gõ /start bình thường
    if payload == "":
        await message.reply_text(
            text=(
                "👋 Chào mừng bạn đến với Bot Support Trading Gold.\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_private_main_menu()
        )
        return

    # Nếu user đi từ group sang bằng deep link
    if payload == "free_signal":
        await message.reply_text(
            text=(
                "📈 NHẬN TÍN HIỆU MIỄN PHÍ\n\n"
                "Bạn đang ở khu vực tín hiệu miễn phí.\n"
                "Chọn mục bên dưới để tiếp tục:"
            ),
            reply_markup=build_free_signal_menu()
        )

    elif payload == "vip_group":
        await message.reply_text(
            text=(
                "💎 NHÓM V.I.P\n\n"
                "Đây là khu vực dành cho người quan tâm đến nhóm V.I.P.\n"
                "Chọn mục bên dưới để xem thêm:"
            ),
            reply_markup=build_vip_menu()
        )

    elif payload == "roadmap":
        await message.reply_text(
            text=(
                "🧭 CHỌN LỘ TRÌNH PHÙ HỢP\n\n"
                "Hãy chọn trạng thái hiện tại của bạn:"
            ),
            reply_markup=build_roadmap_menu()
        )

    elif payload == "contact_admin":
        await message.reply_text(
            text=(
                "☎️ LIÊN HỆ ADMIN\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_contact_menu()
        )

    else:
        await message.reply_text(
            text=(
                "👋 Chào mừng bạn đến với bot Trading Gold.\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_private_main_menu()
        )

# =========================
# 8. XU LY BUTTON TRONG CHAT RIENG
# =========================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()
    data = query.data

    # MENU CHINH TRONG CHAT RIENG
    if data == "private_main_free":
        await query.message.edit_text(
            text=(
                "📈 NHẬN TÍN HIỆU MIỄN PHÍ\n\n"
                "Bạn đang ở khu vực tín hiệu miễn phí.\n"
                "Chọn mục bên dưới để tiếp tục:"
            ),
            reply_markup=build_free_signal_menu()
        )

    elif data == "private_main_vip":
        await query.message.edit_text(
            text=(
                "💎 NHÓM V.I.P\n\n"
                "Đây là khu vực dành cho người quan tâm đến nhóm V.I.P.\n"
                "Chọn mục bên dưới để xem thêm:"
            ),
            reply_markup=build_vip_menu()
        )

    elif data == "private_main_roadmap":
        await query.message.edit_text(
            text=(
                "🧭 CHỌN LỘ TRÌNH PHÙ HỢP\n\n"
                "Hãy chọn trạng thái hiện tại của bạn:"
            ),
            reply_markup=build_roadmap_menu()
        )

    elif data == "private_main_contact":
        await query.message.edit_text(
            text=(
                "☎️ LIÊN HỆ ADMIN\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_contact_menu()
        )

    # FREE SIGNAL
    elif data == "free_read_signal":
        await query.message.edit_text(
            text=(
                "📌 CÁCH ĐỌC TÍN HIỆU\n\n"
                "• Xem rõ điểm Entry\n"
                "• Luôn chú ý Stop Loss\n"
                "• Kiểm tra Take Profit trước khi vào lệnh\n"
                "• Không vào lệnh quá khối lượng"
            ),
            reply_markup=build_free_signal_menu()
        )

    elif data == "free_trade_time":
        await query.message.edit_text(
            text=(
                "🕒 KHUNG GIỜ TRADE ĐẸP\n\n"
                "• Phiên Âu: biến động bắt đầu tốt\n"
                "• Phiên Mỹ: biến động mạnh hơn\n"
                "• Ưu tiên khung giờ có thanh khoản cao"
            ),
            reply_markup=build_free_signal_menu()
        )

    elif data == "free_risk":
        await query.message.edit_text(
            text=(
                "🛡 QUẢN LÝ VỐN CƠ BẢN\n\n"
                "• Không all-in\n"
                "• Mỗi lệnh nên có SL\n"
                "• Rủi ro mỗi lệnh nên nhỏ\n"
                "• Ưu tiên sống sót trước khi nghĩ tới lợi nhuận"
            ),
            reply_markup=build_free_signal_menu()
        )

    # VIP
    elif data == "vip_benefits":
        await query.message.edit_text(
            text=(
                "💎 QUYỀN LỢI NHÓM V.I.P\n\n"
                "• Theo dõi cơ hội tốt hơn\n"
                "• Có định hướng rõ ràng hơn\n"
                "• Phù hợp với người muốn được hỗ trợ sát hơn"
            ),
            reply_markup=build_vip_menu()
        )

    elif data == "vip_fit":
        await query.message.edit_text(
            text=(
                "🎯 AI PHÙ HỢP VỚI V.I.P\n\n"
                "• Người đã có nền tảng cơ bản\n"
                "• Người muốn theo tín hiệu có kỷ luật\n"
                "• Người cần định hướng rõ ràng hơn"
            ),
            reply_markup=build_vip_menu()
        )

    elif data == "vip_join":
        await query.message.edit_text(
            text=(
                "📩 CÁCH THAM GIA V.I.P\n\n"
                "Bạn có thể nhắn admin để được hướng dẫn chi tiết về điều kiện và cách tham gia."
            ),
            reply_markup=build_contact_menu()
        )

    # ROADMAP
    elif data == "roadmap_newbie":
        await query.message.edit_text(
            text=(
                "🌱 BẠN LÀ NGƯỜI MỚI TẬP TRADE VÀNG\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_newbie_menu()
        )

    elif data == "roadmap_experienced":
        await query.message.edit_text(
            text=(
                "🔥 BẠN ĐÃ CÓ KINH NGHIỆM TRADE VÀNG\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_experienced_menu()
        )

    elif data == "newbie_start":
        await query.message.edit_text(
            text=(
                "📘 BẮT ĐẦU TỪ ĐÂU\n\n"
                "• Hiểu vàng chạy mạnh ở phiên nào\n"
                "• Biết Entry, SL, TP là gì\n"
                "• Tập đọc tín hiệu trước khi vào lệnh thật"
            ),
            reply_markup=build_newbie_menu()
        )

    elif data == "newbie_risk":
        await query.message.edit_text(
            text=(
                "💰 QUẢN LÝ VỐN CƠ BẢN\n\n"
                "• Chia vốn nhỏ\n"
                "• Không gồng lệnh tùy tiện\n"
                "• Không tăng lot để gỡ"
            ),
            reply_markup=build_newbie_menu()
        )

    elif data == "newbie_mistakes":
        await query.message.edit_text(
            text=(
                "⛔ LỖI NGƯỜI MỚI HAY MẮC\n\n"
                "• Vào lệnh cảm tính\n"
                "• Không đặt stop loss\n"
                "• Thấy nến chạy là đuổi theo\n"
                "• Trade quá nhiều"
            ),
            reply_markup=build_newbie_menu()
        )

    elif data == "exp_entry":
        await query.message.edit_text(
            text=(
                "🎯 TỐI ƯU ĐIỂM VÀO LỆNH\n\n"
                "• Chờ vùng giá đẹp\n"
                "• Tránh đuổi lệnh\n"
                "• Chỉ vào khi RR hợp lý"
            ),
            reply_markup=build_experienced_menu()
        )

    elif data == "exp_filter_signal":
        await query.message.edit_text(
            text=(
                "📊 LỌC TÍN HIỆU CHẤT LƯỢNG\n\n"
                "• Ưu tiên setup rõ ràng\n"
                "• Chọn tín hiệu đúng thời điểm\n"
                "• Bỏ qua tín hiệu không hợp hệ thống của bạn"
            ),
            reply_markup=build_experienced_menu()
        )

    elif data == "exp_risk":
        await query.message.edit_text(
            text=(
                "⚙️ QUẢN LÝ VỐN NÂNG CAO\n\n"
                "• Kiểm soát drawdown\n"
                "• Không tăng lot vô kế hoạch\n"
                "• Giữ kỷ luật theo chuỗi lệnh"
            ),
            reply_markup=build_experienced_menu()
        )

    # CONTACT
    elif data == "contact_vip":
        await query.message.edit_text(
            text=(
                "💎 HỎI VỀ NHÓM V.I.P\n\n"
                "Bạn có thể nhắn admin để được tư vấn chi tiết về nhóm V.I.P."
            ),
            reply_markup=build_contact_menu()
        )

    elif data == "contact_signal":
        await query.message.edit_text(
            text=(
                "📈 HỎI VỀ TÍN HIỆU\n\n"
                "Nếu bạn cần hiểu rõ hơn cách đọc hoặc theo tín hiệu, hãy nhắn admin để được hướng dẫn."
            ),
            reply_markup=build_contact_menu()
        )

    # BACK
    elif data == "back_private_main":
        await query.message.edit_text(
            text=(
                "👋 Chào mừng bạn đến với bot Trading Gold.\n\n"
                "Chọn mục phù hợp bên dưới:"
            ),
            reply_markup=build_private_main_menu()
        )

    elif data == "back_roadmap":
        await query.message.edit_text(
            text=(
                "🧭 CHỌN LỘ TRÌNH PHÙ HỢP\n\n"
                "Hãy chọn trạng thái hiện tại của bạn:"
            ),
            reply_markup=build_roadmap_menu()
        )

# =========================
# 9. CHAY BOT
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Group: member moi vao
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members)
    )

    # Private chat: /start
    app.add_handler(CommandHandler("start", start_command))

    # Private chat: button
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()