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

$(document).ready(function () {
    // Toggle comments section on comment icon click
    $('.js-comment').click(function () {
        let postId = $(this).data('post-id');
        let commentModal = $('.comment-modal[data-post-id="' + postId + '"]');
        console.log('Toggle comments for post ID:', postId);
        console.log('Comment modal:', commentModal);
        commentModal.toggle();
    });

    $('.comment-form').submit(function (event) {
        event.preventDefault();
    
        let formData = new FormData(this);
    
        console.log('Submitting comment form...');
        console.log('Form data:', formData);
    
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    let newCommentHtml = 
                               '<li class="text-gray-500 bg-white rounded my-2 p-2">' + response.author + ' - ' + response.comment_text + '</li>'
            
                    console.log('Comment submission successful.');
                    console.log('Response:', response);
            
                    let postId = $(event.target).closest('.comment-modal').data('post-id');
                    let commentsSection = $('.comments-section[data-post-id="' + postId + '"]');
            
                    commentsSection.append(newCommentHtml);
            
                    $(event.target).trigger('reset');
                    $('.comment-modal[data-post-id="' + postId + '"]').hide();
                } else {
                    console.error('Error submitting comment:', response.errors);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error submitting comment:', error);
            }
        });
    });

    
    $('.toggle-comments').click(function () {
        let postId = $(this).data('post-id');
        let commentsSection = $('.comments-section[data-post-id="' + postId + '"]');
        commentsSection.toggle('hidden');
    
        // $.ajax({
        //     url: '/post/' + postId + '/comment/',
        //     type: 'GET',
        //     dataType: 'json',
        //     success: function (response) {
        //         if (response.success) {
        //             let commentsHtml = '<ul class="comments-section w-2/4 rounded my-4" data-post-id="' + postId + '">';
                    
        //             response.comments.forEach(function (comment) {
        //                 commentsHtml += '<li class="text-gray-500 bg-white rounded my-1">' + comment.fields.author + ' - ' + comment.fields.text + '</li>';
        //             });
    
        //             commentsHtml += '</ul>';
                    
        //             commentsSection.html(commentsHtml).toggle();
        //         } else {
        //             console.error('Error fetching comments:', response.error);
        //         }
        //     },
        //     error: function (xhr, status, error) {
        //         console.error('Error fetching comments:', error);
        //     }
        // });
    });
});


    


