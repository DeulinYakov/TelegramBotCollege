import handlers as hn


def test1(message, bot):
    hn.cur.execute("SELECT droup, day FROM users WHERE id = ?", (message.chat.id,))
    result = hn.cur.fetchone()
    print("яша крутой" + result[0] + result[1])
    msg = bot.send_message(message.chat.id, result[0] + result[1])
