var PublicDraw = {};

// This function runs when the user make changes in the privacy of a public draw and click "Save" button
// It store the corresponding values in the input field which will be POSTed
PublicDraw.update_privacy_fields = function (){
    var $shared_type_field = $('input#id_shared_type');
    var mode = $('#privacy-selector').attr('data-selected');
    if (mode == "invited"){
        $('#id_password').val("");
        $shared_type_field.attr('value','Invite');
    }else if (mode == "password"){
        var password = $('#draw-password').val();
        $('#id_password').val(password);
        $shared_type_field.attr('value','Public');
    }else{ // Everyone
        $('#id_password').val("");
        $shared_type_field.attr('value','Public');
    }
}

//Initialize the UI to select the level of privacy for the draw
PublicDraw.prepare_privacy_selection = function (){
    // Initialize the UI (slider) to choose the level of restriction of the public draw
    $("#privacy-selector").slideSelector();

    // Initialize button "Save changes". It stores the selection in the form input
    $('button#save-change-privacy').click(function () {
        PublicDraw.update_privacy_fields();
    });
}

PublicDraw.settings = function () {
    // Update the slide selector to show the current level of privacy
    function initialize_slideselector () {
        var current_privacy_level = $('input#id_shared_type').val();
        var password = $('#id_password').val();
        var $privacySelector =  $('#privacy-selector');
        if (current_privacy_level == "Public")
            if (password == "") {
                $privacySelector.slideSelector('select_everyone');
            }
            else {
                $('input#draw-password').val(password);
                $privacySelector.slideSelector('select_password');
            }
        else{
            if (current_privacy_level == "Invite"){
                $privacySelector.slideSelector('select_invited');
            }
        }
    }

    function init_settings_panel(){
        // Show the main settings screen
        $('#settings-general').removeClass("hide");
        $('.settings-submenu').addClass("hide");

        // Remove previous feedback in case they exist
        $('div#public-draw-settings div.feedback').addClass('hide');

        initialize_slideselector();
    }

    // Open settings panel
    $('#settings-button').click(function (){
        init_settings_panel();
    });

    // Show the settings' main screen
    $('.btn-settings-back').click(function (){
        init_settings_panel();
    });

    /*
    SETTINGS OPTION: Edit draw
    Show the confirmation dialog before beginning the edition
    */
    $('li#edit-draw').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-edit-draw').removeClass("hide");
    });

    /*
    SETTINGS OPTION: Edit draw
    Set up the UI to edit a public draw (already published)
    Unlock the fields, hide toss button and present buttons to save changes and cancel the edition
    */
    $('a#edit-draw-confirmation').click(function() {
        PublicDraw.unlock_fields();
        // Hide the toss button
        $('button#toss, #toss-button').addClass('hide');
        // Show the "Save changes" and "Cancel edition" buttons
        $('div#edit-draw-save-changes').removeClass('hide');
        // Close settings panel
        $('#public-draw-settings').modal('hide');
        // Disable Settings button
        $('settings-button').prop( "disabled", true );
    });

    /*
    SETTINGS OPTION: Edit draw
    If the user cancel the draw edition, the page is reloaded.
    */
    $('a#edit-draw-cancel').click(function() {
        // using replace instead on reload to avoid unintentional form submissions
        var url = window.location.href;
        window.location.replace(url);
    });

    /*
    SETTINGS OPTION: Edit draw
    If the has edited a public draw so the configuration is submited to the server
    */
    $('button#edit-draw-save').click(function() {
        $("input[name=submit-type]").val("edit_public_draw");
        return true;
    });

    /*
    SETTINGS OPTION: Invite users
    Show the invitation panel
    */
    $('li#invite').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-invite').removeClass("hide");
    });

    /*
    SETTINGS OPTION: Invite users
    Send the new users to the server
    */
    $('a#send-emails').click(function() {
        $('div#settings-invite div.feedback').addClass('hide');
        var draw_id = $(this).attr("data-id");
        var users = $('input#invite-emails').val();

        // Store the emails in the draw form input
        $('#users').val(users);

        $.get(PublicDraw.url_invite_users, {draw_id: draw_id, emails: users}, function(data){
            $('div#alert-invitation-success').removeClass('hide');
        })
        .fail(function() {
            $('div#alert-invitation-failed').removeClass('hide');
        });
    });

    /*
    SETTINGS OPTION: Change privacy
    Show the privacy panel
    */
    $('li#privacy').click(function() {
        initialize_slideselector();
        $('#settings-general').addClass("hide");
        $('#settings-privacy').removeClass("hide");
    });

    /*
        SAVE SETTINGS
        Send the changes to the server
    */


}

PublicDraw.lock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').prop('readonly', true);

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('readonly');
    $('.protected').parent('.tokenfield').attr('readonly', "true");
}

PublicDraw.unlock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').removeProp('readonly');

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('writeable');
    $('.protected').parent('.tokenfield').removeAttr('readonly');
}


// Initialize the interface for a public draw
PublicDraw.setup = function(current_step){
    //Initialize the UI to select the level of privacy for the draw
    PublicDraw.prepare_privacy_selection();

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    PublicDraw.settings();
    PublicDraw.lock_fields();
}
