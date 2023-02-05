let dark = true;


start_navigation.onclick = function (element) {
  console.log("startNavigation clicked")

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {


    
    fetch("http://127.0.0.1:5000/webscraper", {
      method: "POST",
      body: JSON.stringify({
        url: tabs[0].url
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
      .then(async response => {
        console.log(response)
        tmp = await response.json()
        renderContacts(tmp["delegates"])
      })
     

  })
}

function renderContacts(list) {
  // Get a list of names
  // for each tuple of
  console.log("Function called");
  let contact_list = document.getElementById("scroll_window");
  contact_list.innerHTML = '';

  let count = document.getElementById("count");
    count.textContent=list.length;


  for (i = 0; i < list.length; ++i)
  {
      let el = document.createElement("div");
      el.style.alignSelf="center";
      el.style.padding="5px";
      el.style.height="25px";
      el.style.fontSize="15px";
      if (i % 2 == 0)
      {
          el.style.backgroundColor= "rgba(255, 255, 255, 0.100)";
      }

        // create icon class and twitter icon
        let img1_div = document.createElement("div");
        img1_div.className = "icon";
        img1_div.style.float="right";

        let img1 = new Image(25, 25);
        img1.src = 'img/twitter.png';
        img1_div.appendChild(img1);
        img1_div.style.paddingRight="10px";

        // create icon class and email icon
        let img2_div = document.createElement("div");
        img2_div.className = "icon";
        img2_div.style.float="right";

        let img2 = new Image(25, 25);
        img2.src = 'img/email.png';
        img2_div.appendChild(img2);

        // create email tooltip text and append to icon
        let email_tip = document.createElement("span");
        email_tip.className="tooltiptext";
        email_tip.textContent=list[i][1];
        img2_div.appendChild(email_tip);
        img2_div.addEventListener('click', function() {
            original_text = img2_div.lastChild.textContent;
            navigator.clipboard.writeText(original_text);
            img2_div.lastChild.textContent="Copied!";
            setTimeout(function(){
                img2_div.lastChild.classList.add("fadeOut");
                setTimeout(function(){
                    img2_div.lastChild.classList.remove("fadeOut");
                    img2_div.lastChild.textContent=original_text;
                }, 3000)
            }, 300);
        });

        // create twitter tooltip text and append to icon
        let twitter_tip = document.createElement("span");
        twitter_tip.className="tooltiptext";
        twitter_tip.textContent=list[i][2];
        img1_div.appendChild(twitter_tip);
        img1_div.addEventListener('click', function() {
            original_text = img1_div.lastChild.textContent;
            navigator.clipboard.writeText(original_text);
            img1_div.lastChild.textContent="Copied!";
            setTimeout(function(){
                img1_div.lastChild.classList.add("fadeOut");
                setTimeout(function(){
                    img1_div.lastChild.classList.remove("fadeOut");
                    img1_div.lastChild.textContent=original_text;
                }, 3000)
            }, 300);
        });
        
        el.textContent = list[i][0];
        el.appendChild(img2_div)
        el.appendChild(img1_div);
        contact_list.appendChild(el);
    }
}

$('#mode').on({
    'click':function() {
        if (dark)
        {
            $(this).addClass("rotate");
            dark = false;
            $(this).attr('src', 'img/light.png');
            document.body.style.backgroundColor = "#fcf8f8";
            document.body.style.color = "#333333";
            $("#scroll_window").css({backgroundColor: "#f3effe"});
        }
        else {
            $(this).removeClass("rotate");
            dark = true;
            $(this).attr('src', 'img/night.png');
            document.body.style.backgroundColor = "#121212";
            document.body.style.color = "#f3effe";
            $("#scroll_window").css({backgroundColor: "rgba(255, 255, 255, 0.058)"});
        }
    }
})

const someInput = document.querySelector('icon');

// document.getElementById("start_navigation").onclick = renderContacts;
