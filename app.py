import gradio as gr
from suggestion import generate_outfit_advice
from clothGen import cloth_gen
from user_dress import user_dress
import requests
import os
from io import BytesIO
from PIL import Image
from cal_compatibility import cal_compatibility


gen_pic_num = 6


def get_select_index(evt: gr.SelectData, gallery):
    print(gallery[evt.index][0])
    # response = requests.get(gallery[evt.index][0])
    # img = Image.open(BytesIO(response.content))
    return gallery[evt.index][0]





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
                text_input2 = gr.Textbox(label="身高", min_width=100)
                text_input3 = gr.Textbox(label="体重", min_width=100)
                text_input4 = gr.Textbox(label="腰围", min_width=100)
                text_input5 = gr.Textbox(label="胸围", min_width=100)
                text_input6 = gr.Textbox(label="臀围", min_width=100)
                text_input7 = gr.Textbox(label="肩宽", min_width=100)
                text_input8 = gr.Textbox(label="腿长", min_width=100)
                text_input9 = gr.Textbox(label="臂长", min_width=100)
                dropdown_options1 = ["男", "女"]
                dropdown_input1 = gr.Dropdown(choices=dropdown_options1, label="性别", min_width=100)
                dropdown_options2 = ["胖", "瘦"]
                dropdown_input2 = gr.Dropdown(choices=dropdown_options2, label="体型分类", min_width=100)
                dropdown_options3 = ["黑", "黄", "白"]
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
                # 这里调用模型输出穿搭建议
                submit_button_1.click(fn=generate_outfit_advice,

                                      inputs=[text_input1, text_input2, text_input3, text_input4, text_input5,
                                              text_input6, text_input7, text_input8, text_input9, dropdown_input1,
                                              dropdown_input2, dropdown_input3, text_input10, text_input11, text_input12,
                                              user_pic],
                                      outputs=text_output1)
            image_output_1 = gr.Image(label="显示图像", value="image 209.png")

            gallery_1 = gr.Gallery(
                label="上装", elem_id="gallery",
                value=[
                    # os.path.join(example_path, '上衣/_WEB_2016_09_26__2016092617451357e8ee2957aa1_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717211057ea3a069c749_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717391657ea3e446ce3f_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_27__2016092717573057ea428a305bc_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_28__2016092810150157eb27a56a631_TD.jpg'),
                    # os.path.join(example_path, '上衣/_WEB_2016_09_28__2016092810464557eb2f15e1df3_TD.jpg'),
                ],
                columns=[4], rows=[2], object_fit="contain", height=250, min_width=450)
            # selected = gr.Number(show_label=False, visible=False)


            # gallery_2 = gr.Gallery(
            #     label="下装", elem_id="gallery",
            #     value=[
            #         os.path.join(example_path, '裙/_WEB_2017_01_16__20170116144757587c6c9d6110d_TD.jpg'),
            #         os.path.join(example_path, '裙/_WEB_2017_01_16__20170116150051587c6fa38aa08_TD.jpg'),
            #         os.path.join(example_path, '裙/_WEB_2017_01_16__20170116151007587c71cf63864_TD.jpg'),
            #         os.path.join(example_path, '裙/_WEB_2017_01_16__20170116151641587c7359ab8f3_TD.jpg'),
            #         os.path.join(example_path, '裙/_WEB_2017_01_16__20170116152244587c74c439389_TD.jpg'),
            #         os.path.join(example_path, '裙/_WEB_2017_01_17__20170117120901587d98dd09fd5_TD.jpg'),
            #     ],
            #     columns=[6], rows=[1], object_fit="contain", height=145, min_width=450)
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
                    value=[

                    ],
                    columns=[3], rows=[1], object_fit="contain", height=200, min_width=450)
            with gr.Row():
                submit_button_3 = gr.Button("服饰及搭配兼容性排序")
            with gr.Row():
                image_output_5 = gr.Image(label="显示图像", show_label=False, min_width=300, height=350)
            with gr.Row():
                submit_button_4 = gr.Button("虚拟试穿")
            with gr.Row():
                with gr.Column(scale=1):
                    image_output_6 = gr.Image(label="显示图像", show_label=False, min_width=200, height=350)
                with gr.Column(scale=1):
                    feedback = gr.Textbox(label="反馈", value="可以从款式、颜色、图案、风格倾向、文化偏好角度进行反馈", lines=1,
                                          max_lines=1, elem_id="feedback")
                    submit_button_5 = gr.Button("反馈")
                # com_output = gr.Textbox(label="适配度")

    submit_button_2.click(fn=cloth_gen,
                          inputs=[text_output1, dropdown_input1],
                          outputs=gallery_1)

    gallery_1.select(get_select_index, gallery_1, image_output_5)
    submit_button_3.click(fn=cal_compatibility,
                          inputs=[],
                          outputs=[gallery_4])
    # user_pic_url = user_pic.value['url']
    submit_button_4.click(fn=user_dress,
                          inputs=[user_pic, image_output_5],
                          outputs=image_output_6)
    submit_button_5.click(fn=generate_outfit_advice,
                          inputs=[text_input1, text_input2, text_input3, text_input4, text_input5,
                                  text_input6, text_input7, text_input8, text_input9, dropdown_input1,
                                  dropdown_input2, dropdown_input3, text_input10, text_input11, feedback,
                                  user_pic],
                          outputs=text_output1)

demo.launch(server_port=7860, share=True)
