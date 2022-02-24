import streamlit as st
import pandas as pd
import numpy as np
import decimal
from scipy.stats import beta
from posterior import posterior_plot
from heatmap import heatmap_plot

def runClickTest():
    posterior_file = st.file_uploader("Upload Posterior CSV", type=".csv")
    use_posterior_example_file = st.checkbox(
        "Use example file", False, help="Use in-built example posterior file to demo the app"
    )

    if use_posterior_example_file:
        posterior_file = "./experiment_data.csv"
        ab_default = ['Group']
        result_default = ['Converted']

    if posterior_file:
        experiment_data = pd.read_csv(posterior_file)

        ab_default = None
        result_default = None

        st.write("")
        st.write("")
        st.markdown("#### Uploaded Data Preview")
        st.dataframe(experiment_data.head())

        st.write("")
        st.write("")
        st.markdown("#### Select Columns for Analysis")

        with st.form(key="my_form"):
            ab = st.multiselect(
                "Select Testing Group Column",
                options=experiment_data.columns,
                help="Select which column refers to your control/test testing labels.",
                default=ab_default,
            )
            if ab:
                control = experiment_data[ab[0]].unique()[0]
                test = experiment_data[ab[0]].unique()[1]

                visitors_a = experiment_data[ab[0]].value_counts()[control]
                visitors_b = experiment_data[ab[0]].value_counts()[test]

            result = st.multiselect(
                "Select Conversion Event Column",
                options=experiment_data.columns,
                help="Select which column shows the result of the test.",
                default=result_default,
            )

            if result:
                conversions_a = (
                    experiment_data[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][control]
                )
                conversions_b = (
                    experiment_data[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][test]
                )

            submit_button = st.form_submit_button(label="Submit")

        if not ab or not result:
            st.warning("Please select both an **Testing Group Column** and a **Conversion Event Column**.")
            st.stop()

        name = (
        "./experiment_data.csv" if isinstance(posterior_file, str) else posterior_file.name
        )

        results = experiment_data.groupby('Group').agg({'userId': pd.Series.nunique, 'Converted': sum})
        results.rename({'userId': 'sampleSize'}, axis=1, inplace=True)
        results['conversionRate'] = results['Converted']/results['sampleSize']

        prior_alpha = 1
        prior_beta = 1
        x = np.linspace(0, 1, 1000)

        control = beta(prior_alpha + results.loc['control', 'Converted'], prior_beta + results.loc['control', 'sampleSize'] - results.loc['control', 'Converted'])
        test = beta(prior_alpha + results.loc['test', 'Converted'], prior_beta + results.loc['test', 'sampleSize'] - results.loc['test', 'Converted'])

        lower_bound = results['conversionRate'].min() * 0.5
        upper_bound = results['conversionRate'].max() * 1.5

        x = np.linspace(0, 1, 1000)


        st.write("")
        st.write("")
        st.markdown("#### Test Result Summary")
        st.dataframe(results)
        with st.container():
            plot = posterior_plot(x, control.pdf(x), test.pdf(x), lower_bound, upper_bound)
            st.plotly_chart(plot)

        decimal.getcontext().prec = 4
        control_simulation = np.random.beta(prior_alpha + results.loc['control', 'Converted'], prior_beta + results.loc['control', 'sampleSize'] - results.loc['control', 'Converted'], size=10000)
        test_simulation = np.random.beta(prior_alpha + results.loc['test', 'Converted'], prior_beta + results.loc['test', 'sampleSize'] - results.loc['test', 'Converted'], size=10000)
        test_won = [i <= j for i,j in zip(control_simulation, test_simulation)]
        chance_of_beating_control = np.mean(test_won)


        st.write("")
        st.write("")
        st.markdown(f'### Chance of test beating control is {decimal.getcontext().create_decimal(chance_of_beating_control) * 100} %')

        joint_dist_for_plot = []
        for i in np.linspace(lower_bound,upper_bound,100):
            for j in np.linspace(lower_bound,upper_bound,100):
                joint_dist_for_plot.append([i, j, control.pdf(i)*test.pdf(j)])
        joint_dist_for_plot = pd.DataFrame(joint_dist_for_plot)
        joint_dist_for_plot.rename({0: 'control_cr', 1: 'test_cr', 2: 'joint_density'}, axis=1, inplace=True)
        tick_locations = range(0, 160, 10)
        tick_labels = [round(0.26 + i*0.01, 2) for i in range(16)]
        heatmap_df = pd.pivot_table(joint_dist_for_plot, values='joint_density', index='test_cr', columns='control_cr')

        st.write("")
        st.write("")
        st.markdown("#### Joint Distribution")
        with st.container():
            plot = heatmap_plot(heatmap_df)
            st.plotly_chart(plot)




    # bolttech_colors = {
    # 'white': '#FFFFFF',
    # 'black': '#000000',
    # 'blue_dark': '#160E45',
    # 'cyan_dark': '#00B9C7',
    # 'cyan_medium': '#66D6DD',
    # 'cyan_light': '#CCF1F3',
    # 'yellow_dark': '#E2D900',
    # 'yellow_light': '#F9F7CC',
    # 'grey_dark': '#746F95',
    # 'grey_light': '#D1CFDC'
    # }

    # two_cols = st.checkbox("2 columns?", False)
    # if two_cols:
    #     col1, col2 = st.columns(2)

    # if two_cols:
    #     with col1:
    #         with st.container():
    #             plot = prior_plot(x, prior.pdf(x))
    #             st.plotly_chart(plot)

    #     with col2:
    #         with st.container():
    #             plot = posterior_plot(x, control.pdf(x), test.pdf(x))
    #             st.plotly_chart(plot)

    # else:







    # st.markdown("### Sample Size")
    # nA = st.slider('Sample Size - Control Group', 1, 1000, value = 800)
    # nB = st.slider('Sample Size - Test Group', 1, 1000, value = 800)
    # pA = st.slider('Conversion % - Control Group', 0., 1., value = 0.1, step = 0.01)
    # pB = st.slider('Conversion % - Test Group', 0., 1., value = 0.13, step = 0.01)
    # alpha = st.selectbox("Choose your alpha level", (0.05, 0.01))

    # with st.container():
    #     plot = intro_plot(pA, pB, nA, nB, alpha)
    #     st.plotly_chart(plot)










    # # User choose type
    # chart_type = st.selectbox("Choose your chart type", plot_types)
    # # nA = st.slider('Sample Size - Control Group', 1, 1000, value = 800)
    # # nB = st.slider('Sample Size - Test Group', 1, 1000, value = 800)
    # # alpha = st.selectbox("Choose your alpha level", (0.01, 0.05))

    # # alpha = st.slider('Alpha level', min_value = 0, max_value = 1, value = 0.05, step = 0.01, )


    # with st.container():
    #     st.subheader(f"Showing:  {chart_type}")
    #     st.write("")


    # # create plots
    # def show_plot(kind: str):
    #     st.write(kind)
    #     # if kind == "Matplotlib":
    #     #     plot = matplotlib_plot(chart_type, df)
    #     #     st.pyplot(plot)
    #     # elif kind == "Seaborn":
    #     #     plot = sns_plot(chart_type, df)
    #     #     st.pyplot(plot)
    #     if kind == "Plotly Express":
    #         plot = plotly_plot(chart_type, nA, nB, alpha, df)
    #         st.plotly_chart(plot, use_container_width=True)
    #     elif kind == "Prior":
    #         plot = plotly_plot(chart_type, x, prior.pdf(x))
    #         st.plotly_chart(plot, use_container_width=True)
    #     # elif kind == "Pandas Matplotlib":
    #     #     plot = pd_plot(chart_type, df)
    #     #     st.pyplot(plot)
    #     # elif kind == "Bokeh":
    #     #     plot = bokeh_plot(chart_type, df)
    #     #     st.bokeh_chart(plot, use_container_width=True)
    #     # elif kind == "plotlyGo":
    #     #     plot = plotlyGo_plot(chart_type, df)
    #     #     st.plotlyGo_chart(plot, use_container_width=True)


    # # output plots
    # if two_cols:
    #     # with col1:
    #     #     show_plot(kind="Matplotlib")
    #     with col1:
    #     #    chart_type = st.selectbox("Choose your chart type", plot_types)
    #        nA = st.slider('Sample Size - Control Group', 1, 1000, value = 800)
    #        nB = st.slider('Sample Size - Test Group', 1, 1000, value = 800)
    #        alpha = st.selectbox("Choose your alpha level", (0.01, 0.05))

    #     with col2:
    #         show_plot(kind="Plotly Express")

    #     with col1:
    #         show_plot(kind="Prior")


    #     # with col2:
    #     #     show_plot(kind="Altair")
    #     # with col1:
    #     #     show_plot(kind="Pandas Matplotlib")
    #     # with col2:
    #     #     show_plot(kind="Bokeh")
    #     # with col1:
    #     #     show_plot(kind="plotlyGo")
    # else:
    #     with st.container():
    #         for lib in libs:
    #             show_plot(kind=lib)

    # # display data
    # with st.container():
    #     show_data = st.checkbox("See the raw data?")

    #     if show_data:
    #         df

    #     # notes
    # st.subheader("Notes")
    # st.write(
    #     """
    #     - The graph shows how sample size affects statistical power.
    #     - Imagine you have 10% Of conversion rate under Business as usual and new marketing design has 13% Of conversion rate. Is this result statistically meaningful?
    #     - In usual practice, you are expected to have minimum 80% Of statistical power.
    #     - Play around different sample size with slider at the bottom of the page and see how sample size affects statistical power :)
    #     - Statistical Power = True Positive (THE BIGGER, THE BETTER) - The rate we say 'Yes' and it's true. In other words, statistical power is a chance that we conclude there is a difference between performance of template A and B when there is a actual differnce. In our example, template B achieving 13% Of conversion rate is not by a chance, and we conclude that there is a difference between the two.
    #     - Beta level = False Negative (THE SMALLER, THE BETTER)- The rate we say 'No' but it's false. In other words, there is actual difference between performacne of template A and B, but we conclude there is not. In our example, template B achieving 13% Of conversion rate is not by a chance, however, we conclude it happened by a chance.
    #     - Alpha level =  Significance level - The rate we say 'Yes', but it's false. For our example, there is no actual difference between performance of A and B, but we conclude there is. In our example, template B achieving 13% Of conversion rate is by a chance, however, we think it happened by a chance and conclude it's driven by a coincidence.
    #     """)
    #         # - This app uses [Streamlit](https://streamlit.io/) and the [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) dataset.      
    #         # - To see the full code check out the [GitHub repo](https://github.com/discdiver/data-viz-streamlit).
    #         # - Plots are interactive where that's the default or easy to add.
    #         # - Plots that use Matplotlib under the hood have fig and ax objects defined before the code shown.
    #         # - Lineplots should have sequence data, so I created a date index with a sequence of dates for them. 
    #         # - Where an axis label shows by default, I left it at is. Generally where it was missing, I added it.
    #         # - There are multiple ways to make some of these plots.
    #         # - You can choose to see two columns, but with a narrow screen this will switch to one column automatically.
    #         # - Python has many data visualization libraries. This gallery is not exhaustive. If you would like to add code for another library, please submit a [pull request](https://github.com/discdiver/data-viz-streamlit).
    #         # - For a larger tour of more plots, check out the [Python Graph Gallery](https://www.python-graph-gallery.com/density-plot/) and [Python Plotting for Exploratory Data Analysis](https://pythonplot.com/).
    #         # - The interactive Plotly Express 3D Scatterplot is cool to play with. Check it out! 😎
        
    #         # Made by [Jeff Hale](https://www.linkedin.com/in/-jeffhale/). 
        
    #         # Subscribe to my [Data Awesome newsletter](https://dataawesome.com) for the latest tools, tips, and resources.
        
    #     )