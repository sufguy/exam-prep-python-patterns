import streamlit as st
import reveal_slides as rs

# --- Flyweight Classes ---
class Flyweight:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def operation(self, unique_state):
        return f"Общее: {self.shared_state}, Уникальное: {unique_state}"

class FlyweightFactory:
    def __init__(self):
        self._flyweights = {}

    def get_flyweight(self, shared_state):
        key = tuple(shared_state.items())
        if key not in self._flyweights:
            self._flyweights[key] = Flyweight(shared_state)
        return self._flyweights[key]

# --- Show Slides + Interactive Example ---
def show():
    slide_md = """
    ## Паттерн Flyweight
    Flyweight (легковес) — это структурный паттерн, который позволяет значительно сократить потребление памяти за счёт повторного использования одинаковых объектов, разделяя общее (инвариантное) состояние между ними.
    ---
    ## Проблема
    Когда приложение создаёт большое количество объектов, часто оказывается, что они имеют одинаковые данные. Например, текстовый редактор создаёт объект для каждой буквы — хотя все буквы "а" по сути одинаковы. Это ведёт к:
    - Большому потреблению памяти
    - Повторному хранению одинаковой информации
    - Потере производительности
    ---
    ## Идея паттерна
    Разделить объект на:
    - **Общее состояние (shared state)** — повторяющиеся данные, которые можно хранить один раз и использовать повторно.
    - **Уникальное состояние (unique state)** — данные, которые различаются у каждого объекта.
    Общее состояние кэшируется и передаётся между объектами через фабрику.
    ---
    ## Структура Flyweight
    - **Flyweight** — интерфейс, через который передаётся как общее, так и уникальное состояние
    - **ConcreteFlyweight** — конкретная реализация, содержащая общее состояние
    - **FlyweightFactory** — управляет созданием и хранением объектов Flyweight
    - **Client** — работает с объектами, передавая уникальные параметры
    ---
    ## Реализация: Flyweight-класс
    ```python
    class Flyweight:
        def __init__(self, shared_state):
            self.shared_state = shared_state  # сохраняем общее состояние

        def operation(self, unique_state):
            print(f"Общее: {self.shared_state}, Уникальное: {unique_state}")
    ```
    Здесь `shared_state` хранится внутри объекта и может быть использован многократно. `unique_state` — это данные, зависящие от текущего использования.
    ---
    ## Реализация: фабрика
    ```python
    class FlyweightFactory:
        def __init__(self):
            self._flyweights = {}

        def get_flyweight(self, shared_state):
            key = tuple(shared_state.items())
            if key not in self._flyweights:
                print("Создан новый Flyweight.")
                self._flyweights[key] = Flyweight(shared_state)
            return self._flyweights[key]
    ```
    Фабрика отвечает за кэширование объектов Flyweight по их общему состоянию. Если нужный объект уже есть — возвращается он, иначе создаётся новый.
    ---
    ## Использование: пример
    ```python
    factory = FlyweightFactory()
    fw1 = factory.get_flyweight({"цвет": "красный", "размер": "большой"})
    fw1.operation("позиция 1")

    fw2 = factory.get_flyweight({"цвет": "красный", "размер": "большой"})
    fw2.operation("позиция 2")
    ```
    Вывод покажет, что оба объекта — это один и тот же Flyweight, но с разным уникальным состоянием (позициями).
    ---
    ## Применение на практике
    - Текстовые редакторы (буквы, символы)
    - Системы графики (повторяющиеся текстуры, иконки)
    - Кэширование часто используемых объектов (например, строки, числа)
    - Игра с множеством повторяющихся врагов, пуль и т.п.
    ---
    ## Плюсы и минусы
    **Плюсы:**
    - Существенная экономия памяти при большом количестве объектов
    - Повышение производительности за счёт повторного использования
    - Упрощённое управление состоянием

    **Минусы:**
    - Усложнение архитектуры
    - Требует чёткого отделения общего и уникального состояния
    - Не подходит, если объекты сильно различаются
    ---
    ## Вывод
    Паттерн Flyweight идеален, когда в программе используется множество однотипных объектов. Он повышает эффективность работы с памятью, позволяя хранить общую часть состояния отдельно и использовать её повторно.
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
    st.subheader("🔧 Практический пример: создание и использование Flyweight")

    st.markdown("""
        ### 📘 Инструкция
        1. Выберите **цвет** и **размер** объекта — это будет его **общее состояние**.
        2. Укажите **позицию** — это его **уникальное состояние**.
        3. Нажмите кнопку, чтобы **создать или переиспользовать** объект с выбранным общим состоянием.

        **Зачем это нужно?**  
        Если цвет и размер уже были выбраны раньше — объект **не будет создан заново**.  
        Это демонстрирует, как Flyweight **сохраняет память** и **избегает дублирования**.
        """)

    with st.form("flyweight_form"):
        color = st.selectbox("Выберите цвет", ["красный", "зелёный", "синий"])
        size = st.selectbox("Выберите размер", ["маленький", "средний", "большой"])
        position = st.text_input("Введите уникальную позицию", value="позиция 1")
        submitted = st.form_submit_button("Создать и использовать Flyweight")

    if submitted:
        factory = FlyweightFactory()
        shared = {"цвет": color, "размер": size}
        fly = factory.get_flyweight(shared)
        result = fly.operation(position)
        st.success("✅ Результат:")
        st.code(result)

        # --- Показ исходного кода примера ---
        st.divider()
        st.markdown("### 💻 Исходный код примера:")
        st.code('''
        class Flyweight:
            def __init__(self, shared_state):
                self.shared_state = shared_state

            def operation(self, unique_state):
                return f"Общее: {self.shared_state}, Уникальное: {unique_state}"

        class FlyweightFactory:
            def __init__(self):
                self._flyweights = {}

            def get_flyweight(self, shared_state):
                key = tuple(shared_state.items())
                if key not in self._flyweights:
                    self._flyweights[key] = Flyweight(shared_state)
                return self._flyweights[key]

        # Использование:
        factory = FlyweightFactory()
        shared = {"цвет": "красный", "размер": "большой"}
        fly = factory.get_flyweight(shared)
        print(fly.operation("позиция 1"))
        ''', language="python")


    # --- Служебное: номер слайда и фрагмента ---
    indexf = state.get('indexf', 0)
    st.markdown(f"Слайд {state['indexh']}, фрагмент {indexf}")
