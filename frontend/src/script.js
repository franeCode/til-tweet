const name = userProfileData.name;
const bio = userProfileData.bio;
const coding_stack = userProfileData.coding_stack;


$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document).on("click", ".js-toggle-modal", function(e) {
    e.preventDefault()
    $(".js-modal").toggleClass("hidden")
    console.log("hidden")
})
.on("click", ".js-submit", function(e) {
    e.preventDefault()
    console.log("clicked")
    const text = $(".js-post-text").val().trim()
    console.log(text)
    const $btn = $(this)

    if(!text.length) {
        return false
    }

    $btn.prop("disabled", true).text("Posting!")
    $.ajax({
        type: 'POST',
        url: $(".js-post-text").data("post-url"),
        data: {
            text: text
        },
        success: (dataHtml) => {
            $(".js-modal").addClass("hidden");
            $("#posts-container").prepend(dataHtml);
            $btn.prop("disabled", false).text("New Post");
            $(".js-post-text").val('')
        },
        error: (error) => {
            console.warn(error)
            $btn.prop("disabled", false).text("Error");
        }
    });
})
.on("click", ".js-follow", function(e) {
    e.preventDefault();
    const action = $(this).attr("data-action")

    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action,
            username: $(this).data("username"),
        },
        success: (data) => {
            $(".js-follow-text").text(data.wording)
            if(action == "follow") {
                // Change wording to unfollow
                console.log("DEBUG", "unfollow")
                $(this).attr("data-action", "unfollow")
            } else {
                // The opposite
                console.log("DEBUG", "follow")
                $(this).attr("data-action", "follow")
            }
        },
        error: (error) => {
            console.warn(error)
        }
    });
})
.on("click", ".js-posts-button", function(e) {
    e.preventDefault();
    const url = "{% url 'profiles:detail' user.username %}";
    updatePostsContent(url);
});

$(document).on("click", ".js-following-button", function(e) {
    e.preventDefault();
    const url = "{% url 'profiles:detail' user.username %}";  
    updatePostsContent(url);
});

function updatePostsContent(url) {
    $.ajax({
        type: 'GET', 
        url: url,
        success: (data) => {
            $("#posts-container").html(data.user_posts);
        },
        error: (error) => {
            console.warn(error);
        }
    });
}

$(document).on("click", ".js-toggle-edit", function(e) {
    e.preventDefault()
    $(".js-edit-modal").toggleClass("hidden")

    $("#name").val(name);
    $("#bio").val(bio);
    console.log("hidden")
})

.on("click", ".js-edit", function(e) {
    e.preventDefault();
    const $btn = $(this);
    
    const formData = new FormData($("#editProfileForm")[0]);

    $btn.prop("disabled", true).text("Updating Profile!");
    
    $.ajax({
        type: 'POST',
        url: $("#editProfileForm").attr("action"),  
        data: formData,
        contentType: false,
        processData: false,
        success: (data) => {
            if (data.success) {
                console.log("Profile Updated!");
                $btn.prop("disabled", false).text("Profile Updated!");
                $(".js-edit-modal").addClass("hidden");
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            } else {
                console.warn("Error Updating Profile");
                $btn.prop("disabled", false).text("Error Updating Profile");
            }
        },
        error: (error) => {
            console.warn(error);
            $btn.prop("disabled", false).text("Error Updating Profile");
        }
    });
});