function handleSubmit(event) {
  // 避免瀏覽器執行預設動作, 像是重新整理
  event.preventDefault();

  // 使用內建功能將表單資料轉為[FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData)
  const formData = new FormData(event.target);

  // 輸入欄的型別是字串, 透過parseFloat轉為浮點數
  const height = parseFloat(formData.get("height"));
  const weight = parseFloat(formData.get("weight"));

  // 計算BMI
  const bmi = weight / (height / 100) ** 2;

  // 選取結果區塊
  const resultBox = document.getElementById("result");
  const resultText = resultBox.querySelector("p:first-child"); // 第一個Element
  const resultText2 = resultBox.querySelector("p:last-child"); // 最後一個Element

  // 設定結果文字
  resultText.textContent = "您的BMI為" + bmi.toFixed(2);

  // 判斷BMI結果
  if (isNaN(bmi)) {
    // 當bmi為非數值時
    resultText2.textContent = "請輸入正確的資料";
    resultBox.className = "error";
  } else if (bmi < 18.5) {
    resultText2.textContent = "體重過輕";
    resultBox.className = "underweight";
  } else if (bmi < 24) {
    resultText2.textContent = "正常";
    resultBox.className = "normal";
  } else {
    resultText2.textContent = "體重過重";
    resultBox.className = "overweight";
  }
}

document.querySelector("form").addEventListener("submit", handleSubmit);
