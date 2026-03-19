import { messages } from "../i18n";

const email = messages.email;

const digitalDownloadTemplate = `
doctype html
html
    head
        style(type='text/css').
            .cta-container {
                margin: 32px 0px;
                text-align: center;
            }
            .cta {
                border: 1px solid #07077b;
                border-radius: 4px;
                padding: 4px 8px;
                text-decoration: none;
                color: white;
                background-color: #07077b;
                font-weight: bold;
            }
            .cta:hover {
                background-color: #060665;
            }
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
        p   ${email.download_thanks.replace("{courseName}", "#{courseName}")}
        div(class="cta-container") 
            a(
                href=\`\${downloadLink}\`
                class="cta"
            ) ${email.download_button}
        p   ${email.download_best}
        p   #{name}
        p 
            |   ${email.course_enroll_access} 
            |   #[a(href=\`\${loginLink}\`) ${email.course_enroll_login}] ${email.course_enroll_here}
        if !hideCourseLitBranding
            div(class="courselit-branding-container")
                a(
                    href="https://courselit.app"
                    target="_blank"
                    class="courselit-branding-cta"
                ) ${email.powered_by} <strong> CourseLit </strong>
`;

export default digitalDownloadTemplate;
