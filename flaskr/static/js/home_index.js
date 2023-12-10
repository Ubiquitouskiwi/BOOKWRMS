var addTagButton = document.querySelector(".add-tag-button")
addTagButton.onclick = function () {
    var modalBookIdInput = document.querySelector("#modal_book_id");
    modalBookIdInput.value = addTagButton.id;
}