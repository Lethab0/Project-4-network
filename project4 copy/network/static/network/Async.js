//import { doUntil } from "async";

document.addEventListener("DOMContentLoaded" , function() {



  var dict = {
    FirstName: "Chris",
    id : 1
  };

  
  Get_likes(dict);
  Edit();

})


function Get_likes(post) {
  fetch(`/liked/${post.id}`)
  .then(response => response.json())
  .then(posts_info => {
    // Print email
  
    var heart_count = document.querySelectorAll(".like_count");
    var heart_shape = document.querySelectorAll(".likes");
    var text_info = document.querySelectorAll(".post_text");
    var like_span = document.querySelectorAll(".like_objects");

    for (i = 0; i < heart_count.length; i++) {

      for (k = 0 ; k < posts_info.length ; k++) {
        if (parseInt(heart_count[i].id) === posts_info[k].id) {
          heart_count[i].innerHTML = posts_info[k].likes;
          if (posts_info[k].user_like === true ){
            heart_shape[i].style.color = "red";
          }
          

        }
        let current_likebutton = heart_shape[i];
        current_likebutton.onclick = function() {
          let post = current_likebutton.id;
          Liking(current_likebutton.style.color ,post);
          heart_color(post, current_likebutton);
        };
        
        }
        
    }

 
});
}

function heart_color(post , element){
  if (post.who_liked === true) {
    element.style.color = "blue";
  }
}

/// sending Api information for liking and unliking
function Liking(btn_color , post_id) {
  let user = document.querySelector("Strong");
  let current_user = user.id;

  if (btn_color === "red") {
    console.log("red") ;
    let liked = true;

    //Sending the info
    fetch(`/like_or_unlike/${post_id}`, {
      method: 'POST',
      body: JSON.stringify({
          user: current_user,
          liked: liked
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);      
  });

    Get_likes(post_id);   
 
  } else {
    console.log("blue")
    let liked = false;

    //Sending the info
    fetch(`/like_or_unlike/${post_id}`, {
      method: 'POST',
      body: JSON.stringify({
          user: current_user,
          liked: liked,
     
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result

        var dict = {
          FirstName: "Chris",
          id : 1
        };
      
        
        Get_likes(dict);
        console.log(result);
        Get_likes(post_id);
        print("hello");
    });

    var dict = {
      FirstName: "Chris",
      id : 1
    };
  
    
    Get_likes(dict);
    Get_likes(post_id);
    console.log("hello");
  }
   
  
}

function Edit(){
  fetch(`/Edit_posts`)
  .then(response => response.json())
  .then(Edit_info => {
    
    var text_info = document.querySelectorAll(".post_text");
    let like_span = document.querySelectorAll(".like_objects");

    // cycle through all the posts
    for (i = 0; i < text_info.length; i++) {
      let edit_btn = document.createElement("button");  // the edit button
  
      // Cycle through the fetched info about the posts
      for (k = 0 ; k < Edit_info.length ; k++){
        let currnt_post_text = text_info[i];
       
        // if the post and post dat match check if the post can be edited
        if (parseInt(currnt_post_text.id) === Edit_info[k].Post_id) {
          console.log(`${currnt_post_text.id} : ${Edit_info[k].Post_id}` );
          if (Edit_info[k].Edit === true) {
            // create a button if its changeable
            console.log(true);
            edit_btn.innerHTML = "Edit";
            
            let the_text = text_info[i].innerHTML;
            let text_order = i;
            let text_id = text_info[i].id;
            if (edit_btn.id === "active"){
              console.log("of");
            }
            
            edit_btn.onclick = () => {
              Edit_Text(the_text, text_order, text_id ,edit_btn);
              edit_btn.id = "active";
              console.log(edit_btn.id);
              edit_btn.disabled = true;
            }
            
            like_span[i].appendChild(edit_btn);
                     
          }
        }
        
      }
    }
  });
}

function Edit_Text(text, text_number ,text_id ,edit_btn){
  let all_texts = document.querySelectorAll(".post_text");
  let like_span = document.querySelectorAll(".like_objects");
  console.log(all_texts);

  all_texts[text_number].innerHTML = '';
  let tex_box = document.createElement("textarea");
  tex_box.innerText = text;
  all_texts[text_number].appendChild(tex_box);

  // Create the save button
  
  let save_btn = document.createElement("button");
  save_btn.innerHTML = "Save";
  

  //The asyncronous saving process
  save_btn.onclick = () => {
    let new_text = tex_box.value;
    
    fetch(`/Edit/${text_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          text: new_text
      })
    });

    //reload data
    all_texts[text_number].innerHTML = new_text;
    like_span[text_number].removeChild(save_btn);
    edit_btn.disabled = false;
  }

  // add and display the save button 
  like_span[text_number].appendChild(save_btn);
  

}