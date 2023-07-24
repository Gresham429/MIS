window.onload = () => {
    const form1 = document.querySelector("#addForm");
    const loginButton = document.getElementById("loginButton");
    
    let items = document.getElementById("items");
    let submit = document.getElementById("submit");
  
    let editItem = null;
  
    form1.addEventListener("submit", addItem);
    items.addEventListener("click", removeItem);
    loginButton.addEventListener("click", handleLogin);
};
  
function addItem(e) {
    e.preventDefault();

    let teamName = document.getElementById("item").value.trim();
    let teamLeader = document.getElementById("teamLeader").value.trim();

    if (teamName === "")
        return false;

    let li = document.createElement("li");
    li.className = "list-group-item";

    let deleteButton = document.createElement("button");
    deleteButton.className = "btn-danger btn btn-sm float-right delete";
    deleteButton.appendChild(document.createTextNode("Delete"));

    let editButton = document.createElement("button");
    editButton.className = "btn-success btn btn-sm float-right edit";
    editButton.appendChild(document.createTextNode("Edit"));

    let listItemText = "团队：" + teamName;
    if (teamLeader !== "")
        listItemText += "，队长：" + teamLeader;

    li.appendChild(document.createTextNode(listItemText));
    li.appendChild(deleteButton);
    li.appendChild(editButton);

    items.appendChild(li);

    document.getElementById("item").value = "";
    document.getElementById("teamLeader").value = "";

    return false;
}

 
function removeItem(e) {
    e.preventDefault();
    if (e.target.classList.contains("delete")) {
        if (confirm("Are you Sure?")) {
            let li = e.target.parentNode;
            items.removeChild(li);
            document.getElementById("lblsuccess").innerHTML
                = "Text deleted successfully";
  
            document.getElementById("lblsuccess")
                        .style.display = "block";
  
            setTimeout(function() {
                document.getElementById("lblsuccess")
                        .style.display = "none";
            }, 3000);
        }
    }
    if (e.target.classList.contains("edit")) {
        document.getElementById("item").value =
            e.target.parentNode.childNodes[0].data;
        submit.value = "EDIT";
        editItem = e;
    }
}
  
function toggleButton(ref, btnID) {
    document.getElementById(btnID).disabled = false;
} 

function handleLogin() {
    // 在这里实现登录逻辑，例如弹出登录框或跳转到登录页面等
    alert("Login button clicked!");
}
