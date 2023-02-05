//let list = [["Bill", "bill123@gmail.com", "haha"], ["Harley", "sshihhung21@vt.edu", "haha"], ["Jayson", "jaysond21@vt.edu", "haha"], ["Joe", "joemama@aol.com", "haha"], ["Clinton", "clinton2@gmail.com", "haha"]];


start_navigation.onclick = function (element) {
    console.log("startNavigation clicked")
  
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
  
          
          const delegateList = fetch("http://127.0.0.1:5000/webscraper", {
              method: "POST",
              body: JSON.stringify({
                url : tabs[0].url
              }),
              headers: {
                "Content-type": "application/json; charset=UTF-8"
              }
            });

            let list = delegateList
            renderContacts()
          
      })
  }

function renderContacts() {
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
        el.style.fontSize="20px";
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
        img2_div.addEventListener("click", function(el){
            text = img2_div.lastChild.textContent;
            navigator.clipboard.writeText(text);
            img2_div.lastChild.textContent = "Copied!";
        });

        // create twitter tooltip text and append to icon
        let twitter_tip = document.createElement("span");
        twitter_tip.className="tooltiptext";
        twitter_tip.textContent=list[i][2];
        img1_div.appendChild(twitter_tip);
        img1_div.addEventListener("click", function(el){
            text = img1_div.lastChild.textContent;
            navigator.clipboard.writeText(text);
            img1_div.lastChild.textContent = "Copied!";
        });

        
        el.textContent = list[i][0];
        el.appendChild(img2_div)
        el.appendChild(img1_div);
        contact_list.appendChild(el);
    }
}

const someInput = document.querySelector('icon');

document.getElementById("settings").onclick = renderContacts;
