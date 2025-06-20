import streamlit as st
import reveal_slides as rs

# --- Handler classes ---
class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, request):
        if self.successor:
            return self.successor.handle(request)
        else:
            return f"🚫 Никто не обработал: {request}"

class AdminHandler(Handler):
    def handle(self, request):
        if request.lower() == "admin":
            return "✅ Обработано обработчиком: admin"
        return super().handle(request)

class UserHandler(Handler):
    def handle(self, request):
        if request.lower() == "user":
            return "✅ Обработано обработчиком: user"
        return super().handle(request)

class GuestHandler(Handler):
    def handle(self, request):
        if request.lower() == "guest":
            return "✅ Обработано обработчиком: guest"
        return super().handle(request)

# --- Show slides + interactive demo ---
def show():
    slide_md = """
    ## Chain of Responsibility
    Цепочка обязанностей — поведенческий паттерн, позволяющий передавать запрос по цепочке объектов-обработчиков. Каждый обработчик решает, обрабатывать ли запрос или передать дальше.
    ---
    ## Проблема
    Когда в коде много условий вида:
    ```python
    if type == "admin":
        handle_admin()
    elif type == "user":
        handle_user()
    elif type == "guest":
        handle_guest()
    ```
    Это:
    - Жёстко связывает обработку с конкретными условиями
    - Плохо масштабируется
    - Усложняет поддержку
    ---
    ## Идея паттерна
    Создать "цепочку обработчиков", в которой каждый знает только о следующем звене. Запрос передаётся от одного к другому, пока кто-то его не обработает.
    ---
    ## Участники
    - **Handler** — базовый интерфейс с методом `handle(request)`
    - **ConcreteHandler** — конкретные обработчики запроса
    - **Client** — создаёт цепочку и передаёт запрос первому обработчику
    ---
    ## Реализация: базовый обработчик
    ```python
    class Handler:
        def __init__(self, successor=None):
            self.successor = successor

        def handle(self, request):
            if self.successor:
                return self.successor.handle(request)
            else:
                return f"Никто не обработал: {request}"
    ```
    ---
    ## Реализация: конкретные обработчики
    ```python
    class AdminHandler(Handler):
        def handle(self, request):
            if request == "admin":
                return "Обработано: admin"
            return super().handle(request)

    class UserHandler(Handler):
        def handle(self, request):
            if request == "user":
                return "Обработано: user"
            return super().handle(request)
    ```
    ---
    ## Пример использования
    ```python
    h3 = Handler()
    h2 = UserHandler(successor=h3)
    h1 = AdminHandler(successor=h2)

    print(h1.handle("user"))
    print(h1.handle("guest"))
    ```
    ---
    ## Применение на практике
    - Middleware в веб-фреймворках (Flask, Django)
    - Обработка событий в UI (нажатия кнопок, перемещения мыши)
    - Логгеры (уровень DEBUG → INFO → WARNING → ERROR)
    ---
    ## Плюсы и минусы
    **Плюсы:**
    - Уменьшение связности между компонентами
    - Гибкость: можно легко менять порядок обработчиков
    - Лёгкое расширение: просто добавь новый обработчик

    **Минусы:**
    - Нет гарантии, что запрос будет обработан
    - Может быть сложно отследить, где именно он обработался
    ---
    ## Вывод
    Chain of Responsibility помогает выстроить гибкую и масштабируемую обработку запросов. Особенно полезен там, где возможна последовательная проверка условий без жёсткой привязки.
    """

    state = rs.slides(
        slide_md,
        height=600,
        theme="black",
        config={"plugins": ["highlight", "notes", "zoom"]},
        markdown_props={"data-separator-vertical": "^--$"}
    )

    # --- Интерактивный пример ---
    st.divider()
    st.subheader("🔧 Практический пример: передача запроса по цепочке")

    st.markdown("""
    ### 📘 Инструкция
    1. Введите тип пользователя: `admin`, `user`, `guest` или любой другой.
    2. Нажмите кнопку — запрос пойдёт по цепочке обработчиков.
    3. Вы увидите, **кто из обработчиков** обработал ваш запрос, или что никто не смог.

    **Зачем это нужно?**  
    Это показывает, как работает цепочка: если один обработчик не может — он передаёт запрос дальше.
    """)

    with st.form("chain_form"):
        user_input = st.text_input("Введите тип запроса (admin / user / guest / другое)", value="user")
        submitted = st.form_submit_button("Отправить запрос в цепочку")

    if submitted:
        chain = AdminHandler(UserHandler(GuestHandler()))
        result = chain.handle(user_input)
        st.success("✅ Результат обработки:")
        st.code(result)

    # --- Показ исходного кода примера ---
    st.divider()
    st.markdown("### 💻 Исходный код примера:")
    st.code('''
class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, request):
        if self.successor:
            return self.successor.handle(request)
        else:
            return f"🚫 Никто не обработал: {request}"

class AdminHandler(Handler):
    def handle(self, request):
        if request.lower() == "admin":
            return "✅ Обработано обработчиком: admin"
        return super().handle(request)

class UserHandler(Handler):
    def handle(self, request):
        if request.lower() == "user":
            return "✅ Обработано обработчиком: user"
        return super().handle(request)

class GuestHandler(Handler):
    def handle(self, request):
        if request.lower() == "guest":
            return "✅ Обработано обработчиком: guest"
        return super().handle(request)

# Использование:
chain = AdminHandler(UserHandler(GuestHandler()))
print(chain.handle("user"))
''', language="python")

    # --- Текущий слайд и фрагмент ---
    indexf = state.get("indexf", 0)
    st.markdown(f"Слайд {state['indexh']}, фрагмент {indexf}")
