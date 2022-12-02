import os
import sys

import streamlit as st
import wandb
from dotenv import find_dotenv, load_dotenv

from model.title_optimizer import title_optimizer

sys.path.insert(0, "..")

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
assert os.getenv("OPENAI_API_KEY"), "No OPENAI_API_KEY defined in .env."


project_name = "GPT-3 blog title"
run = wandb.init(project=project_name, job_type="prompting", resume=True)

artifact = run.use_artifact(f"benneo/{project_name}/fine_tune_details:v1", type="fine_tune_details")

fine_tuned_model = artifact.metadata["fine_tuned_model"]


def main():

    st.title("GPT-3 Blog Title Optimizer")
    st.markdown(
        """
        Enter a blog title and click the button to generate 6 optimized titles with scores
        """
    )
    with st.form(key="title_form"):
        title_input = st.text_input(label="Blog Title")
        temp = st.slider("Temperature", 0.0, 1.0, 0.5)
        st.markdown(
            "[What is"
            " temperature?](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277)"
        )
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:

        if title_input == "":
            st.error("Please enter a title")
            return

        out, out_html = title_optimizer(fine_tuned_model, title_input, temp)

        st.dataframe(out_html, use_container_width=True)

        prediction_table = wandb.Table(columns=["Title", "Good Prob"], data=out)
        wandb.log({"predictions": prediction_table})


if __name__ == "__main__":

    main()
