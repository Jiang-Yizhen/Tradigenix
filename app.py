import gradio as gr
from sugg_gene import suggest_gene
from clothGen import cloth_gen
from user_dress import user_cloths
import requests
import os
from io import BytesIO
from PIL import Image
from cal_compatibility import cal_compatibility


gen_pic_num = 6
save_directory = "downloads"


def get_select_index(evt: gr.SelectData, gallery):
    print(gallery[evt.index][0])
    with open(os.path.join(save_directory, f"cloth_intro_{evt.index//2+1}.txt"), "r") as f:
        introduction = f.read()
    return gallery[evt.index][0], introduction


def update_choices(dropout1, dropout2,):
    if dropout1 == "男":
        option = ['倒三角形', '矩形', '苹果形', '沙漏型', '胖型']
    else:
        option = ["梨形", "草莓形", "沙漏形", "标准", "苹果形"]
    dropout2 = gr.Dropdown(choices=option)
    return dropout2


with gr.Blocks(css="styles.css", theme=gr.themes.Base()) as demo:
    with gr.Row():
        # 左侧模块
        with gr.Column(scale=1):
            with gr.Row():
                gr.Markdown(""
                            "# 用户信息"
                            "")
            with gr.Row():
                text_input1 = gr.Textbox(label="用户姓名", min_width=100)
                text_input2 = gr.Textbox(label="身高/cm", min_width=100)
                text_input3 = gr.Textbox(label="体重/kg", min_width=100)
                text_input4 = gr.Textbox(label="腰围/cm", min_width=100)
                text_input5 = gr.Textbox(label="胸围/cm", min_width=100)
                text_input6 = gr.Textbox(label="臀围/cm", min_width=100)
                text_input7 = gr.Textbox(label="肩宽/cm", min_width=100)
                text_input8 = gr.Textbox(label="腿长/cm", min_width=100)
                text_input9 = gr.Textbox(label="臂长/cm", min_width=100)
                dropdown_options1 = ["女", "男"]
                dropdown_input1 = gr.Dropdown(choices=dropdown_options1, label="性别", min_width=100)
                dropdown_input2 = gr.Dropdown(choices=["梨形", "草莓形", "沙漏形", "标准", "苹果形"], label="体型分类", min_width=100)
                dropdown_input1.change(fn=update_choices, inputs=[dropdown_input1, dropdown_input2], outputs=dropdown_input2)
                dropdown_options3 = ["浅色", "中等偏黄色", "中等偏褐色", "深色"]
                dropdown_input3 = gr.Dropdown(choices=dropdown_options3, label="肤色", min_width=100)
                text_input10 = gr.Textbox(label="穿衣风格偏好", min_width=1000)
                text_input11 = gr.Textbox(label="生话方式和场景需求", min_width=1000)
                text_input12 = gr.Textbox(label="其他特殊需求", min_width=1000)
            with gr.Row():
                user_pic = gr.Image(label="用户照片", value="model.jpg", height=550, width=300)

        # 右侧模块
        with gr.Column(scale=2):
            with gr.Row():
                gr.Markdown(""
                            "# 穿搭建议"
                            "")
            with gr.Row():
                text_output1 = gr.Textbox(label="穿搭建议", lines=12, max_lines=12, interactive=False, show_label=False,
                                          min_width=1000)
                submit_button_1 = gr.Button("AI智能分析，生成穿搭建议", min_width=1000)
            image_output_1 = gr.Image(label="显示图像", value="image 209.png")

            gallery_1 = gr.Gallery(
                label="服装", elem_id="gallery", interactive=False,
                value=[
                    # os.path.join(example_path, '上衣/_WEB_2016_09_26__2016092617451357e8ee2957aa1_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717211057ea3a069c749_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717391657ea3e446ce3f_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717573057ea428a305bc_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_28__2016092810150157eb27a56a631_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_28__2016092810464557eb2f15e1df3_TD.jpg'),
                ],
                columns=[4], rows=[2], object_fit="contain", height=250, min_width=450)

            gallery_3 = gr.Gallery(
                label="配饰", elem_id="gallery",
                value=[
                    'downloads/access_1.jpg',
                    'downloads/access_2.jpg',
                    'downloads/access_3.jpg',
                    'downloads/access_4.jpg',
                    'downloads/access_5.jpg',
                    'downloads/access_6.jpg',
                ],
                columns=[4], rows=[2], object_fit="contain", height=250, min_width=450)
            submit_button_2 = gr.Button("AI智能分析，生成民族服饰")

        with gr.Column(scale=2):
            with gr.Row():
                gr.Markdown(""
                            "# 搭配生成"
                            "")
            with gr.Row():
                gallery_4 = gr.Gallery(
                    label="套装", elem_id="gallery",
                    value=[],
                    columns=[3], rows=[1], object_fit="contain", height=180, min_width=450)
            with gr.Row():
                submit_button_3 = gr.Button("服饰及搭配兼容性排序")
            with gr.Row():
                image_output_5 = gr.Image(label="显示图像", show_label=False, min_width=200, height=350, interactive=False)
                intro = gr.Textbox(label="服饰介绍", lines=14, max_lines=14)
            with gr.Row():
                gallery_user = gr.Gallery(
                    label="试穿结果",
                    elem_id="gallery",
                    value=[],
                    columns=[3], rows=[2],
                    object_fit="contain",
                    min_width=200,
                    height=350,
                )
            with gr.Row():
                submit_button_4 = gr.Button("虚拟试穿")
            with gr.Row():
                feedback = gr.Textbox(label="反馈", placeholder="可以从款式、颜色、图案、风格倾向、文化偏好角度进行反馈", lines=1,
                                      max_lines=1, elem_id="feedback")
            with gr.Row():
                submit_button_5 = gr.Button("反馈")
    with gr.Row():
        gr.Markdown("""
                    女性体型备注：
                    1. **梨形身材**：臀围比胸围**至少大5.08厘米**
                    2. **草莓形身材**：臀围比胸围**至少小5.08厘米**
                    3. **沙漏形身材**：胸围比腰围**至少大3.81厘米**且腰部线条明显
                    4. **标准身材**：胸围比腰围**至少大3.81厘米**且腰部线条不明显
                    5. **苹果形身材**：胸围比腰围**至少小3.81厘米**
                    
                    男性体型备注：
                    1. **倒三角形身材**：肩宽比腰围**至少大10厘米**  
                    2. **矩形身材**：肩宽与腰围的差异**小于5厘米**  
                    3. **苹果形身材**：腰围比肩宽**至少大7.5厘米**  
                    4. **沙漏型身材**：腰围比肩宽或臀围**至少小10厘米**，且肩宽和臀围的差异**小于5厘米**  
                    5. **胖型身材**：腰围比胸围或肩宽**至少大10厘米**
                    """)

    submit_button_1.click(fn=suggest_gene,
                          inputs=[text_input1, text_input2, text_input3, text_input4, text_input5,
                                  text_input6, text_input7, text_input8, text_input9, dropdown_input1,
                                  dropdown_input2, dropdown_input3, text_input10, text_input11, text_input12,
                                  feedback, user_pic],
                          outputs=[text_output1])
    submit_button_2.click(fn=cloth_gen,
                          inputs=dropdown_input1,
                          outputs=[gallery_1, image_output_5, intro])

    gallery_1.select(fn=get_select_index, inputs=gallery_1, outputs=[image_output_5, intro])
    submit_button_3.click(fn=cal_compatibility,
                          inputs=[],
                          outputs=[gallery_4])
    submit_button_4.click(fn=user_cloths,
                          inputs=[user_pic, image_output_5],
                          outputs=gallery_user)
    submit_button_5.click(fn=suggest_gene,
                          inputs=[text_input1, text_input2, text_input3, text_input4, text_input5,
                                  text_input6, text_input7, text_input8, text_input9, dropdown_input1,
                                  dropdown_input2, dropdown_input3, text_input10, text_input11, text_input12,
                                  feedback, user_pic],
                          outputs=[text_output1])

demo.launch(server_port=7860, share=True)
