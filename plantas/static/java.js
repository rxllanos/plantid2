document.addEventListener("DOMContentLoaded", function () {

  document.querySelectorAll(".btn-primary").forEach(button => {
      button.addEventListener("click", function () {
          let id = button.getAttribute("data-id");
          let info = button.getAttribute("data-info");
          console.log("Opening First Modal - Data:", { id, info });
          handledata(id, info);
      });
  });

  let healthContainer = document.getElementById("container2"); // Ensure this element exists
  healthContainer.addEventListener("click", function (event) {
      if (event.target.classList.contains("modal2")) {
          let id = event.target.dataset.id;
          let info = event.target.dataset.info;
          console.log("Disease Button Clicked! Attributes:", event.target.dataset);
          handledata(id, info);  // Now this function will run properly
      }
  });

  let ingredientContainer = document.getElementById("container3"); // Ensure this element exists
  ingredientContainer.addEventListener("click", function (event) {
      if (event.target.classList.contains("modal3")) {
          let id = event.target.dataset.id;
          let info = event.target.dataset.info;
          console.log("Ingredient Button Clicked! Attributes:", event.target.dataset);
          handledata(id, info);  // Now this function will run properly
      }
  });

  document.querySelectorAll(".btn-close").forEach(button => {
    button.addEventListener("click", function () {
      setTimeout(() => {
        location.reload(); // Reload after modal is closed
      }, 300); // Small delay to allow modal to close smoothly
    });
  });

});

const parseJsonField = (field) => {
  try {
      let fixedField = field.replace(/'\b(?!\s)/g, '"').replace(/\b(?!\s)'/g, '"');
      return JSON.parse(fixedField);
  } catch (error) {
      console.error(`Error parsing field: ${field}`, error);
      return ["Parsing error: Invalid JSON format"];
  }
};

async function handledata(id, info) {
  document.getElementById("container1").innerHTML = "";
  document.getElementById("container2").innerHTML = "";
  document.getElementById("container3").innerHTML = "";
  document.getElementById("container4").innerHTML = "";
  if (info === 'Plant_Information') {
      Plant(id);
      Ingredient(id);
  }
  if (info === 'Disease') {
    Disease(id);
  }
  if (info === 'Nutrition'){
    Nutrition(id);
  }
  if (info === 'Recepy'){
    Recepy(id);
  }
}

async function Plant(id){
  try {
    const response = await fetch(`/planta/api/plantadata/${id}/`);
    const plant = await response.json();
    const plantContainer = document.getElementById("container1");

    if (!plant || typeof plant !== "object") {
      console.error("Unexpected response:", plant);
      return;
    }
    const commonNames = parseJsonField(plant.plant_data_common_names);
    const edibleParts = parseJsonField(plant.plant_data_edible_parts);
    const propagationMethods = parseJsonField(plant.plant_data_propagation_methods);
    const card = document.createElement("div");

    card.innerHTML = `
    <div class="card-body">
        <h5 class="card-title">${plant.plant_data_name}</h5>
        <img src="${plant.plant_data_image}" class="img-fluid rounded-start" alt="${plant.plant_data_name}">
        <p class="text-muted">Probability: ${(plant.plant_data_probability * 100).toFixed(2)}%</p>
        <p><strong>Taxonomy:</strong> ${plant.plant_data_taxonomy}</p>
        <p><strong>GBIF ID:</strong> ${plant.plant_data_gbif_id} | <strong>iNaturalist ID:</strong> ${plant.plant_data_inaturalist_id}</p>
        <p><strong>Common Names:</strong> ${commonNames.join(", ")}</p>
        <p><strong>Edible Parts:</strong> ${edibleParts.join(", ")}</p>
        <p><strong>Propagation Methods:</strong> ${propagationMethods.join(", ")}</p>
        <p><strong>Watering:</strong> ${plant.plant_data_watering_min} - ${plant.plant_data_watering_max} (scale)</p>

        <a href="${plant.plant_data_url}" target="_blank" class="btn btn-primary btn-sm">Learn More</a>
    </div>
    `;
    plantContainer.appendChild(card);

    const response1 = await fetch(`/planta/api/plantahealth/${id}/`);
    const data1 = await response1.json();
    const percentage = data1.health_is_healthy_probability;
    heatlhContainer = document.getElementById("container2");
    const formattedPercentage = (percentage).toLocaleString(undefined, {
      style: 'percent',
      minimumFractionDigits: 2,
    });
    heatlhContainer.innerHTML = `The plant is healthy? ${data1.health_is_healthy_binary}, probability of healthy: ${formattedPercentage}`;
    
    if(data1.health_is_healthy_binary===false){
      try {
        let newButton = document.createElement("button");
        newButton.setAttribute("type", "button");
        newButton.setAttribute("data-toggle", "modal");  // Bootstrap 5 uses data-bs-toggle
        newButton.setAttribute("data-target", "#exampleModal2");
        newButton.setAttribute("data-id", id);  // Example ID
        newButton.setAttribute("data-info", "Disease");
        newButton.classList.add("btn", "modal2");
        newButton.innerText = "Likely Diseases.";
        heatlhContainer.appendChild(newButton);
        console.log("Button Disease Created:", newButton.dataset);
      }  
      catch (error) {
        console.error("Caught an error:", error.message);
      } finally {
          console.log("This will always execute, regardless of an error.");
      }

    }
  }  
  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }
}

async function Ingredient(id) {
  try {
    const response = await fetch(`/planta/api/plantaingredient/${id}/`);
    const ingredients = await response.json();
    const ingredientContainer = document.getElementById("container3");

    // Clear the container before adding new elements
    ingredientContainer.innerHTML = "";

    ingredients.forEach(async (ingredient) => {
      const possibleUnits = parseJsonField(ingredient.ingredient_possible_units);
      console.log(`${ingredient.ingredient_original_name}`);

      const card = document.createElement("div");
      card.className = ""; 
      card.innerHTML = `
          <div class="card-body">
              <hr>
              <img src="${ingredient.ingredient_img}" class="img-fluid rounded-start" alt="${ingredient.ingredient_original_name}">
              <h5 class="card-title">${ingredient.ingredient_original_name}</h5>
              <p><strong>Amount:</strong> ${ingredient.ingredient_amount} ${ingredient.ingredient_unit}</p>
              <p><strong>Possible Units:</strong> ${possibleUnits.join(", ")}</p>
              <p><strong>Consistency:</strong> ${ingredient.ingredient_consistency}</p>
              <p><strong>Estimated Cost:</strong> ${ingredient.ingredient_estimated_cost_value} ${ingredient.ingredient_estimated_cost_unit}</p>
          </div>
      `;

      let newButton1 = document.createElement("button");
      newButton1.setAttribute("type", "button");
      newButton1.setAttribute("data-toggle", "modal");  // Bootstrap 5 uses data-bs-toggle
      newButton1.setAttribute("data-target", "#exampleModal2");
      newButton1.setAttribute("data-id", ingredient.ingredient_original_name);  // Example ID
      newButton1.setAttribute("data-info", "Nutrition");  // Example ID
      newButton1.classList.add("btn", "modal3");
      newButton1.innerText = "Nutrition facts!";
      card.appendChild(newButton1);
      console.log("Button Nutrition  Created:", newButton1.dataset);



      let newButton2 = document.createElement("button");
      newButton2.setAttribute("type", "button");
      newButton2.setAttribute("data-toggle", "modal");  // Bootstrap 5 uses data-bs-toggle
      newButton2.setAttribute("data-target", "#exampleModal2");
      newButton2.setAttribute("data-id", ingredient.ingredient_original_name);  // Example ID
      newButton2.setAttribute("data-info", "Recepy");
      newButton2.classList.add("btn", "modal3");
      newButton2.innerText = "Recepies!";
      card.appendChild(newButton2);      
      console.log("Button Recepy Created:", newButton2.dataset);

      ingredientContainer.appendChild(card);
    });
  }          
  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }  
}

async function Disease(id){
  try {
    diseaseContainer = document.getElementById("container4");
    const response2 = await fetch(`/planta/api/plantadesease/${id}/`);
    const diseases = await response2.json();
    diseases.forEach(disease => {
        const diseaseCard = document.createElement("div");
        diseaseCard.innerHTML = `
            <hr>
            <h4>${disease.disease_name} (Probability: ${(disease.disease_probability * 100).toFixed(2)}%)</h4>
            <p><strong>Description:</strong> ${disease.disease_description}</p>
            <p><strong>Cause:</strong> ${disease.disease_cause || "Unknown"}</p>
            <p><strong>Common Names:</strong> ${disease.disease_common_names_disease ? disease.disease_common_names_disease.join(", ") : "N/A"}</p>
            <p><strong>Health Assessment:</strong> ${disease.disease_health_assessment}</p>
            <p><strong>Treatment (Chemical):</strong> ${disease.disease_treatment_chemical.join("<br>")}</p>
            <p><strong>Treatment (Biological):</strong> ${disease.disease_treatment_biological.join("<br>")}</p>
            <p><strong>Prevention:</strong> ${disease.disease_prevention.join("<br>")}</p>
            <a href="${disease.disease_url}" target="_blank">More Info</a>
        `;  
        diseaseContainer.appendChild(diseaseCard);
    });  
  }
  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }  
}

async function Nutrition(id){
  try {
    const nutritionContainer = document.getElementById("container4");
    nutritionContainer.innerHTML = "";
    let ingredient = id
    const ingredientName = ingredient;
    const response1 = await fetch(`/planta/api/plantan/${ingredientName}/`);
    const nutrientData = await response1.json();
    const response2 = await fetch(`/planta/api/plantap/${ingredientName}/`);
    const propertyData = await response2.json();
    const response3 = await fetch(`/planta/api/plantaf/${ingredientName}/`);
    const flavonoidData = await response3.json();
    const response4 = await fetch(`/planta/api/plantacbd/${ingredientName}/`);
    const caloricBreakdownData = await response4.json();
    const response5 = await fetch(`/planta/api/plantawps/${ingredientName}/`);
    const weightPerServingData = await response5.json();

    const nutritiondiv = document.createElement("div");
    nutritiondiv.innerHTML = `
    <hr>
        <div class="card-body">
            <table class="table table-bordered">
                <tr><th>Property</th><td>${propertyData.map(p => `${p.property_name}: ${p.property_amount} ${p.property_unit}`).join('<br>')}</td></tr>
                <tr><th>Nutrient</th><td>${nutrientData.map(n => `${n.nutrient_name}: ${n.nutrient_amount} ${n.nutrient_unit} (${n.nutrient_percent_of_daily_needs}% of daily needs)`).join('<br>')}</td></tr>
                <tr><th>Flavonoid</th><td>${flavonoidData.map(f => `${f.flavonoid_name}: ${f.flavonoid_amount} ${f.flavonoid_unit}`).join('<br>')}</td></tr>
                <tr><th>Caloric Breakdown</th><td>Protein: ${caloricBreakdownData.cb_percent_protein}%, Fat: ${caloricBreakdownData.cb_percent_fat}%, Carbs: ${caloricBreakdownData.cb_percent_carbs}%</td></tr>
                <tr><th>Weight Per Serving</th><td>${weightPerServingData.wps_amount} ${weightPerServingData.wps_unit}</td></tr>
            </table>
        </div>
    `;
    nutritionContainer.appendChild(nutritiondiv);

  }
  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }  
}


async function Recepy(id){
  let ingredient = id
  try {
    const RecepyContainer = document.getElementById("container4");
    RecepyContainer.innerHTML = "";
    const response = await fetch(`/planta/api/ingredientrecepy/${ingredient}/`);
    const recipes = await response.json();
    recipes.forEach(recipe => {
      const card = document.createElement('div');
      card.classList.add('recipe-card');
      
      card.innerHTML = `
      <img src="${recipe.recepy_image}" alt="${recipe.recepy_title}" class="recipe-image" onerror="this.onerror=null;this.src='https://via.placeholder.com/100?text=No+Image';">
          <h4>${recipe.recepy_title}</h4>
          <p>Used Ingredients: ${recipe.recepy_used_ingredient_count}</p>
          <p>Missed Ingredients: ${recipe.recepy_missed_ingredient_count}</p>
          <div class="ingredient-list" id="ingredients-${recipe.id}" style="display: none;"></div>
      `;
      RecepyContainer.appendChild(card);

      const response1 = fetch(`/planta/api/recepyingredient/${recipe.recepy_id_recepy}/`);
      const ingredients = response1.json();
      ingredients.forEach(ing => {
          const item = document.createElement('div');
          item.classList.add('ingredient-item');
          item.innerHTML = `
              <img src="${ing.ingrecepy_image}" alt="${ing.ingrecepy_name}" class="ingredient-image">
              <p>${ing.ingrecepy_amount} ${ing.ingrecepy_unit} ${ing.ingrecepy_name}</p>
          `;
          RecepyContainer.appendChild(item);

          
      });
  });   

  }
  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }  
}

async function RecepyIng(id){
  try {
      const response1 = await fetch(`/planta/api/recepyingredient/${id}/`);
      const ingredients = await response1.json();
      ingredients.forEach(ing => {
          const item = document.createElement('div');
          item.classList.add('ingredient-item');
          item.innerHTML = `
              <img src="${ing.ingrecepy_image}" alt="${ing.ingrecepy_name}" class="ingredient-image">
              <p>${ing.ingrecepy_amount} ${ing.ingrecepy_unit} ${ing.ingrecepy_name}</p>
          `;
          RecepyContainer.appendChild(item);
      });
  }

  catch (error) {
    console.error("Caught an error:", error.message);
  } finally {
      console.log("This will always execute, regardless of an error.");
  }  
}