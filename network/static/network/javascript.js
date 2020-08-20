document.addEventListener('DOMContentLoaded', function() {
    follow =  document.querySelector('#follow');
    unfollow = document.querySelector('#unfollow');
    followers = document.querySelector('#followers');

    document.querySelectorAll('.fa-edit').forEach((edit_button) => {
        edit_button.onclick = () => {
            post_id = edit_button.dataset.id;
            cancel = document.querySelector(`#close_${post_id}`);
            after_edit = document.querySelector(`#after_edit_${post_id}`);
            oldtext =  document.querySelector(`#old_text_${post_id}`);
            textarea =  document.querySelector(`#edit_post_${post_id}`);
            editform = document.querySelector(`#editform_${post_id}`);
            post = document.querySelector(`#post_${post_id}`);
            newpost = document.querySelector('.new_post');

            document.querySelectorAll('.post').forEach((posts) => {
                posts.style.filter = "blur(2px)";
                posts.style.pointerEvents = "none";
            });
            newpost.style.filter = "blur(2px)";
            newpost.style.pointerEvents = "none";
            post.style.filter = "blur(0px)";
            post.style.pointerEvents = "auto";
            post.style.boxShadow = "0px 0px 30px orange";

            edit_button.style.display = 'none';
            after_edit.style.display = 'block';
            oldtext.style.display = 'none';
            textarea.value = oldtext.innerHTML;
            editform.style.display = 'block';

            cancel.onclick = () => {
                edit_button.style.display = 'block';
                after_edit.style.display = 'none';
                oldtext.style.display = 'block';
                editform.style.display = 'none';
                document.querySelectorAll('.post').forEach((posts) => {
                    posts.style.filter = "none";
                    posts.style.pointerEvents = "auto";
                });
                newpost.style.filter = "none";
                newpost.style.pointerEvents = "auto";
                post.style.boxShadow = "none";
            }

            editform.onsubmit = () => {
                edit_button.style.display = 'block';
                after_edit.style.display = 'none';
                oldtext.innerHTML = textarea.value;
                oldtext.style.display = 'block';
                editform.style.display = 'none';
                document.querySelectorAll('.post').forEach((posts) => {
                    posts.style.filter = "none";
                    posts.style.pointerEvents = "auto";
                });
                newpost.style.filter = "none";
                newpost.style.pointerEvents = "auto";
                post.style.boxShadow = "none";
                submit_edit(post_id);
                return false;
            }
        }
    });
    document.querySelectorAll('.fa-thumbs-up').forEach((like_button) => {
        like_button.onclick = () => {
            post_id = like_button.dataset.id;
            if(like_button.title == "LIKE")
            {
                document.querySelector(`#likes_${post_id}`).innerHTML++;
                like_button.title = "UNLIKE";
                like_button.style.color = "#fd8f00";
                like(post_id);
            }
            else
            {
                document.querySelector(`#likes_${post_id}`).innerHTML--;
                like_button.title = "LIKE";
                like_button.style.color = "";
                unlike(post_id);
            }
        }
    });
    follow.onclick = () => {
        follow.style.display = 'none';
        unfollow.style.display = 'inline-block';
        count = followers.innerHTML;
        count++;
        followers.innerHTML = count;
        username = follow.dataset.username;
        follow_func(username);
    };
    unfollow.onclick = () => {
        unfollow.style.display = 'none';
        follow.style.display = 'inline-block';
        count = followers.innerHTML;
        count--;
        followers.innerHTML = count;
        username = unfollow.dataset.username;
        unfollow_func(username);
    };
        
});

function like(post_id)
{
    fetch(`/like/${post_id}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => console.log(data));
}
function unlike(post_id)
{
    fetch(`/unlike/${post_id}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => console.log(data));
}
function submit_edit(post_id)
{
    fetch(`/edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector(`#edit_post_${post_id}`).value
        })
    })
    .then(response => response.json())
    .then(data => console.log(data));
    return false;
}
function follow_func(username)
{
    fetch(`/follow/${username}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => console.log(data));
}
function unfollow_func(username)
{
    fetch(`/unfollow/${username}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => console.log(data));
}