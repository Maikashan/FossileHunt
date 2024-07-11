window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        press_bone_button: function() {
            bone_button = document.querySelector('.bone-button');
            if (bone_button) {
                bone_button.click();
            }
            return window.dash_clientside.no_update;
        }
    }
});
