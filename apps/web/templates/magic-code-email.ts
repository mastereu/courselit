import { messages } from "../i18n";

const email = messages.email;

const magicCodeEmail = `
doctype html
html
    head
        style(type='text/css').     
            .courselit-branding-container {
                margin: 40px 0px;
            }
            .courselit-branding-cta {
                text-decoration: none;
                color: #000000;
                padding: 6px 10px;
                background-color: #FFFFFF;
                border: 1px solid;
                border-radius: 6px;
                text-align: center;
            }
    body
        p   #{code} ${email.magic_code_body.replace("{code}", "").trim()}
        p
            strong ${email.magic_code_important}
            |   ${email.magic_code_warning}
        if !hideCourseLitBranding
            div(class="courselit-branding-container")
                a(
                    href="https://courselit.app"
                    target="_blank"
                    class="courselit-branding-cta"
                ) ${email.powered_by} <strong> CourseLit </strong>
`;

export default magicCodeEmail;
