const btn_tool = document.querySelector('#btn-tool');
const tool_menu = document.querySelector('#tool-menu');
const btn_tool_close = document.querySelector('#btn-tool-close');

btn_tool.addEventListener('click', () => {
    tool_menu.classList.toggle('disp');
    btn_tool.classList.toggle('disp');
    btn_tool_close.classList.toggle('disp');
});

btn_tool_close.addEventListener('click', () => {
    tool_menu.classList.toggle('disp');
    btn_tool.classList.toggle('disp');
    btn_tool_close.classList.toggle('disp');
});