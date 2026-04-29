# Импорт необходимых библиотек
import streamlit as st
import altair as alt
from streamlit_echarts import st_echarts
import pandas as pd
from PIL import Image

# Иконка приложения
im = Image.open("icon_mortgage.png")

# Функция расчётов
def calc(realty_cost, down_payment, rate, credit_period):
    # Расчёты
    # Сумма кредита
    S = realty_cost - down_payment
    # Месячная процентная ставка
    r = rate / 12 / 100
    # Количество месяцев
    n = credit_period * 12
    # Ежемесячный платеж
    x = S * ((r * (1 + r) ** n) / ((1 + r) ** n - 1))
    # Общая сумма выплат
    X = x * n
    # Переплата по кредиту
    overpayment = X - S
    # Рекомендуемый доход
    income_recommended = x / 0.3
    # Налоговый вычет
    tax_realty_deduction = min(260_000, realty_cost * 0.13)
    tax_mortgage_interest_deduction = min(390_000, overpayment * 0.13)
    tax_deduction = tax_realty_deduction + tax_mortgage_interest_deduction

    return x, S, overpayment, X, income_recommended, tax_deduction, tax_realty_deduction, tax_mortgage_interest_deduction

# Настройка страницы
st.set_page_config(
    page_title="Ипотечный калькулятор",
    page_icon=im,
    layout="wide"
)

# Наименование
st.title("Ипотечный калькулятор")
st.markdown("Удобный ипотечный калькулятор - быстро и удобно рассчитать на калькуляторе ежемесячный платёж и другие метрики.")

with st.container(border=True, key="main_container"):
    # Выбор ипотечной программы
    type_hypothec = st.pills(
        label=None,
        options=[
            "Стандартная",
            "Семейная ипотека",
            "IT ипотека",
            "Дальневосточная/Арктическая ипотека"
        ],
        selection_mode="single",
        default="Стандартная",
        required=True,
        key="type_hypothec"
    )
    # Определение ставки в зависимости от ипотечной программы
    if type_hypothec == "Стандартная":
        rate_default = 16.0
    elif type_hypothec == "Семейная ипотека":
        rate_default = 6.0
    elif type_hypothec == "IT ипотека":
        rate_default = 6.0
    elif type_hypothec == "Дальневосточная/Арктическая ипотека":
        rate_default = 2.0

    col_data, col_metric = st.columns([60, 40], border=False)
    # Ввод данных
    with col_data:
        col1, col2 = st.columns(2, border=True)
        with col1:
            # Стоимость недвижимости
            realty_cost = st.number_input(
                label="Стоимость недвижимости, ₽",
                min_value=0,
                max_value=None,
                value=5_000_000,
                step=100_000,
                format="%d",
                key="realty_cost"
            )
            st.write("Стоимость недвижимости:", f"{realty_cost:,} ₽".replace(",", " "))

        with col2:
            # Первоначальная стоимость
            down_payment = st.number_input(
                label="Первоначальный взнос, ₽",
                min_value=0,
                value=1_000_000,
                step=50_000,
                format="%d"
            )
            st.write("Первоначальный взнос:", f"{down_payment:,} ₽".replace(",", " "))

        col1, col2 = st.columns(2, border=True)
        with col1:
            # Процентная ставка
            rate = st.number_input(
                label="Процентная ставка, %",
                min_value=0.0,
                max_value=99.0,
                value=rate_default,
                step=0.1,
                format="%f"
            )
        with col2:
            # Срок в годах
            credit_period = st.select_slider(
                label="Срок кредита, г.",
                options=[m + 1 for m in range(30)],
                value=5
            )

    with col_metric:
        if realty_cost < down_payment:
            st.error("Первоначальный взнос должен быть меньше стоимости недвижимости!")
            st.stop()
        # Вычисления
        x, S, overpayment, X, income_recommended, tax_deduction, tax_realty_deduction, tax_mortgage_interest_deduction = calc(
            realty_cost=realty_cost,
            down_payment=down_payment,
            rate=rate,
            credit_period=credit_period
        )
        # Вывод метрик
        col1, col2 = st.columns(2, border=False)
        with col1:
            formatted_x = f"{round(x):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                  <div style="font-weight:700; color:#4285b4; font-size:32px;">{formatted_x}</div>
                  <div style="font-size:12px; color:#474A51;margin-top:-4px;">Ежемесячный платёж</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            formatted_overpayment = f"{round(overpayment):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                    <div style="font-weight:700; color:#2e2e2e; font-size:32px;">{formatted_overpayment}</div>
                    <div style="font-size:12px; color:#474A51;margin-top:-4px;">Переплата по кредиту</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            formatted_income_recommended = f"{round(income_recommended):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                    <div style="font-weight:700; color:#2e2e2e; font-size:32px;">{formatted_income_recommended}</div>
                    <div style="font-size:12px; color:#474A51;margin-top:-4px;">Рекомендуемый доход</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            formatted_S = f"{round(S):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                    <div style="font-weight:700; color:#2e2e2e; font-size:32px;">{formatted_S}</div>
                    <div style="font-size:12px; color:#474A51;margin-top:-4px;">Сумма кредита</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            formatted_X = f"{round(X):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                    <div style="font-weight:700; color:#2e2e2e; font-size:32px;">{formatted_X}</div>
                    <div style="font-size:12px; color:#474A51;margin-top:-4px;">Общая сумма выплата</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            formatted_tax_deduction = f"{round(tax_deduction):,} ₽".replace(",", " ")
            st.markdown(
                f"""
                <div style="text-align:left">
                    <div style="font-weight:700; color:#2e2e2e; font-size:32px;">{formatted_tax_deduction}</div>
                    <div style="font-size:12px; color:#474A51;margin-top:-4px;">Налоговый вычет</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Дополнительно: графики
with st.expander(label="Графики", icon=":material/chart_data:"):
    col1, col2 = st.columns([60, 40], border=False)
    with col1:
        def create_amortization_schedule(principal, annual_rate, months):
            """Возвращает DataFrame с помесячным графиком погашения"""
            monthly_rate = annual_rate / 12 / 100
            if monthly_rate == 0:  # Безпроцентная ипотека
                payment = principal / months
                data = []
                balance = principal
                for m in range(1, months + 1):
                    balance -= payment
                    data.append({
                        "month": m,
                        "payment": payment,
                        "principal": payment,
                        "interest": 0,
                        "balance": max(0, balance)
                    })
                return pd.DataFrame(data)

            payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

            schedule = []
            balance = principal
            for month in range(1, months + 1):
                interest = balance * monthly_rate
                principal_payment = payment - interest
                balance -= principal_payment
                schedule.append({
                    "month": month,
                    "payment": payment,
                    "principal": principal_payment,
                    "interest": interest,
                    "balance": max(0, balance),
                    "year": (month - 1) // 12 + 1  # Для группировки по годам
                })
            return pd.DataFrame(schedule)

        # Подготовка данных
        df_amort = create_amortization_schedule(
            principal=S,
            annual_rate=rate,
            months=credit_period * 12
        )

        # Построение графика
        chart_amort = alt.Chart(df_amort).transform_fold(
            ["principal", "interest"],
            as_=["component", "amount"]
        ).transform_calculate(
            component_ru="datum.component == 'principal' ? 'Тело кредита' : 'Проценты'",
            amount_formatted="replace(format(datum.amount, ',.0f'), ',', ' ')",
            payment_formatted="replace(format(datum.payment, ',.0f'), ',', ' ')"
        ).mark_area(opacity=0.8).encode(
            x=alt.X("month:Q", title="Месяц", axis=alt.Axis(grid=False, values=list(range(0, len(df_amort) + 1, 12)), format="d")),
            y=alt.Y(
                "amount:Q",
                title="Сумма, ₽",
                stack="zero",
                axis=alt.Axis(
                    grid=False,
                    labelExpr="replace(format(datum.value, ',.0f'), ',', ' ')"
                )
            ),
            color=alt.Color(
                "component_ru:N",
                scale=alt.Scale(domain=["Тело кредита", "Проценты"], range=['#cccccc', '#9b1827']),
                legend=alt.Legend(
                    title=None,
                    orient="top",
                    direction="horizontal",
                    symbolType="square",
                    labelFontSize=10,
                    titleFontSize=12
                )
            ),
            tooltip=[
                alt.Tooltip("month:Q", title="Месяц"),
                alt.Tooltip("component_ru:N", title="Компонент"),
                alt.Tooltip('amount_formatted:N', title='Сумма'),
                alt.Tooltip('payment_formatted:N', title='Всего платёж')
            ]
        ).properties(
            title="Структура платежей",
            width="container",
            height=350
        ).configure_title(
            fontSize=16,
            font="Helvetica, Arial, sans-serif",
            color="#2e2e2e",
            anchor="start",
            offset=-10
        ).configure_text(
            font="Helvetica, Arial, sans-serif",
            color="#474A51",
            fontSize=12
        ).configure_axis(
            labelFont="Helvetica, Arial, sans-serif",
            titleFont="Helvetica, Arial, sans-serif",
            labelColor="#474A51",
            titleColor="#474A51",
            tickColor="#474A51"
        ).configure_legend(
            orient="top",
            labelLimit=200,
            titleFont="Helvetica, Arial, sans-serif",
            labelFont="Helvetica, Arial, sans-serif",
            labelColor="#474A51"
        )

        st.altair_chart(chart_amort, use_container_width=True)

    with col2:
        def fmt_rub_py(n: int) -> str:
            return f"{n:,}".replace(",", " ") + " ₽"
        options = {
            "title": {
                "text": "Налоговый вычет",
                "left": "left",
                "top": "0px",
                "textStyle": {
                    "fontFamily": "Helvetica, Arial, sans-serif",
                    "color": "#2e2e2e",
                    "fontSize": 16,
                    "fontWeight": "bold"
                }
            },
            "legend": {
                "data": ["Стоимость недвижимости", "Уплаченные проценты"],
                "top": "30px",
                "left": "0%",
                "orient": "horizontal",
                "fontSize": 12
            },
            "grid": {"left": "0px", "top": "25px", "bottom": "0px", "containLabel": True},
            "xAxis": {
                "type": "value",
                "splitLine": {"show": False},
                "axisLabel": {"show": False},
                "axisLine": {"show": False},
                "axisTick": {"show": False}
            },
            "yAxis": {
                "type": "category",
                "data": ["Налоговый вычет"],
                "splitLine": {"show": False},
                "axisLabel": {"show": False},
                "axisLine": {"show": False},
                "axisTick": {"show": False}
            },
            "series": [
                {
                    "name": "Стоимость недвижимости",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position": "inside",
                        "formatter": "{c}",
                        "color":"#ffffff"
                    },
                    "itemStyle": {"color": "#3da8cb"},
                    "emphasis": {"focus": "series"},
                    "data": [{"value": v, "label": {"show": True, "formatter": fmt_rub_py(v)}} for v in [round(tax_realty_deduction)]]
                },
                {
                    "name": "Уплаченные проценты",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position": "inside",
                        "formatter": "{c}",
                        "color": "#ffffff"
                    },
                    "itemStyle": {"color": "#9b3281"},
                    "emphasis": {"focus": "series"},
                    "data": [{"value": v, "label": {"show": True, "formatter": fmt_rub_py(v)}} for v in [round(tax_mortgage_interest_deduction)]]
                },
            ],
            "tooltip": {
                "trigger": "item",
                "formatter": "{a}: {c} ₽"
            },
            "textStyle": {
                "fontFamily": "Helvetica, Arial, sans-serif",
                "color": "#474A51"
            }
        }
        st_echarts(options=options, height="340px")