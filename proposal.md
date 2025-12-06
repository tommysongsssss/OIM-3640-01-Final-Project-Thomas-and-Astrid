# Project Proposal  

**Course:** OIM3640 – Problem Solving & Software Design  
**Team Members:** Thomas Song & Astrid Yuan  
**Date:** November 14  

---

## 1. The Big Idea

Both Thomas and Astrid have studied abroad where they faced a lot of traveling around Europe very frequently. Although traveling is exciting, packing is universally painful—people overpack, forget essentials, misunderstand weather patterns, and waste time second-guessing what to bring. 

Especially when Thomas was studying abroad in London, he was unaware that places in Europe use a different type of electrical cord plug and therefore he was unable to charge his devices when he was traveling in Europe for the first time. Another time, Thomas packed a lot of heavy winter clothes when he traveled to Tenerife during the winter but realized that Tenerife is tropical all year round after he landed. Astrid experienced many similar challenges while studying abroad in Barcelona，where traveling within Europe required extensive planning. Budget-friendly flights often came with strict luggage restrictions, making it essential to pack efficiently within a carry-on.

Our project aims to solve this problem with an **AI Trip Packing Assistant**: a Python-based tool that automatically generates a smart, optimized packing list for any trip. Rather than relying on generic online lists, our assistant will tailor recommendations to the user’s specific destination, dates, and planned activities.

The core idea is that the user will input their destination and trip dates, and then select their planned activities from a multiple-choice list of common travel purposes. Users may choose more than one option, since a single trip can involve multiple types of activities. The initial activity options will include:

A. City sightseeing
B. Hiking or outdoor excursions
C. Business meetings or formal events
D. Sports or recreational activities (e.g., volleyball)
E. Beach or pool vacation
Etc...

This structured activity selection will help the program tailor packing recommendations more accurately.

Once this information is provided, the program will:

- Fetch real-time and, if useful, historical weather forecasts using a weather API such as **Open-Meteo** or **OpenWeather**.  
- Interpret temperature ranges, precipitation probability, and overall climate patterns across the trip window in order to characterize each day as, for instance, *hot and dry*, *cold and rainy*, or *mild and cloudy*.  

Based on this weather interpretation and the user’s activity profile, the program will generate a **personalized packing checklist**. This list will cover categories such as:

- Clothing  
- Footwear  
- Hygiene items  
- Electronics  
- Optional items (for example, electrical adapters, portable chargers, rain jackets, swimwear, or business attire)

As a **stretch goal**, the assistant will also be able to provide **weather-specific outfit recommendations**, grouping items into suggested daily combinations such as:

> “One warm base layer, one mid-layer, waterproof shell, and waterproof boots”  

for a cold, rainy hiking day. Another stretch goal is to offer an **export feature** that converts the packing list into a cleanly formatted **PDF** that users can save or print.

The **Minimum Viable Product (MVP)** is a fully functional command-line (`CLI`) application that allows the user to enter their destination and trip dates and then returns useful, reliable information. For the MVP, the program will:

- Fetch weather data  
- Output a simple daily weather summary  
- Generate a basic packing list derived from clear climate logic (for example, more warm layers for colder destinations and more light clothing for hot locations)

The stretch goals will be built on top of this MVP once the core functionality is stable and tested.

---

## 2. Learning Objectives

Because this is a team project with two members, Thomas and Astrid, we have both **shared** and **individual** learning objectives.

At a **shared level**, we want to deepen our ability to use Python to solve real-world problems in a structured way and incorporate a lot of the knowledge that Professor Li has taught us. This includes:

- Learning how to interact with external APIs  
- Handling JSON responses  
- Integrating external data into our own program logic  
- Decomposing a project into modules  
- Designing clear function interfaces  
- Writing code that is readable and maintainable  

Another shared goal is to strengthen our comfort with:

- Debugging and testing  
- Using version control as part of a **collaborative workflow** rather than as solo programmers  

This will also be the **first time** Thomas and Astrid have created an extensive project using APIs where it is also the first project that solves an issue we are both passionate about.

At an **individual** level:

- **Astrid** would like to focus more heavily on the *backend logic* of the project. This includes:
  - Implementing and testing the weather API integration (fetching and parsing forecast/climate data).
  - Designing and refining decision rules that map weather, trip length, and activity inputs into packing recommendations.
  - Exploring different ways to represent these rules in code (e.g., configuration dictionaries, helper functions, or simple classes).
  - Improving skills in writing *testable* functions, with clear inputs/outputs and sample cases for validation.


- **Thomas** is especially interested in working with *external services and output formatting*. This includes getting comfortable with making HTTP requests, handling potential errors or missing data from APIs, and then transforming program output into user-friendly formats such as nicely structured terminal text and, if possible, PDF files.  

Both of us also want to practice thinking about **user experience**, even in a CLI environment, by making input prompts clear, error messages helpful, and output easy to understand at a glance.

---

## 3. Implementation Plan

Our implementation will begin with **research and experimentation**.

First, we will compare at least two candidate weather APIs (likely **Open-Meteo** and **OpenWeather**) to understand:

- Their documentation  
- Authentication requirements  
- Rate limits  
- The format and granularity of the data they return  

We will write a small **prototype script** that sends a request for a single sample city and date range, then prints out the raw JSON response. From this, we will decide which fields (such as daily minimum and maximum temperature, precipitation chances, and weather conditions) are most useful for our logic and which API best fits our needs and constraints.

Once we have selected an API and identified the relevant fields, we will design a **weather interpretation module**. This module will take the raw API response and turn it into a simplified representation that our program can reason about. For example, it might assign each day labels such as:

- “cold,” “moderate,” or “hot” (based on temperature thresholds)  
- “dry” or “rainy” (based on precipitation probability)  

and note any special conditions such as storms or extreme weather. We will also consider how to **aggregate this information** across the entire trip duration to decide, for example, how many cold-weather outfits or rain-ready outfits the user should pack.

In parallel, we will design the **packing logic engine**. This subsystem will take as input:

- The interpreted weather profile  
- The length of the trip  
- The user’s activity description  

It will then apply a set of **rule-based heuristics** to generate a packing list. For example:

- Allocate a certain number of shirts, pairs of pants, and socks based on trip length and temperature  
- Add extra layers and outerwear for cold climates  
- Add swimwear for beach trips  
- Include business attire for professional travel  

We will initially **hard-code** these rules in Python but keep them organized and well-documented so they can be refined later if we have time.

### Optimization and Outfit Logic

We plan to “automatically generate an optimized packing checklist and suggested outfits” using **rule-based logic** driven by weather and trip length. First, we will bucket each day into climate categories (for example, cold/dry, cold/rainy, mild, or hot) based on temperature and precipitation thresholds. Then, for each category, we will map to clothing needs (such as *one base layer + one mid-layer + one outer layer* for cold days, or *one light top + one bottom* for hot days) and scale item counts with trip length while capping them to encourage re-wear. For instance, we might use rules like `shirts = ceil(days / 2)`, `underwear = days`, and `shoes = 1–2` depending on activities. In this context, “optimized” means covering all expected weather scenarios and activities with the **fewest reasonable items**, reducing overpacking while still being practical. Finally, the outfit feature will assemble these items into day-by-day combinations by pulling from the appropriate category sets (for example, a “cold rainy hiking outfit” would be built from a warm base layer, a fleece or mid-layer, a waterproof shell, hiking pants, and waterproof shoes).

Once the weather interpretation and packing logic modules are working in isolation, we will build the **command-line interface (CLI)** that ties everything together. The CLI will:

1. Guide the user through entering their destination, trip dates, and planned activities  
2. Validate that the inputs are sensible  
3. Orchestrate calls to the API and internal modules  
4. Print a clear summary of the expected weather and the recommended packing list  

After the MVP is functioning, we will explore **stretch features** such as:

- A simple outfit recommendation layer that groups individual clothing items into combinations  
- A PDF export function that uses a Python library to generate a nicely formatted document  

Throughout this process, we will write **basic tests** for our key functions and handle common error cases, such as invalid city names or unrealistic date ranges.

---

## 4. Project Schedule

We have roughly **four to five weeks** to complete this project, so we plan to structure our work in phases and try not to be too ambitious with our planning. However, if we do finish things faster than we planned, we will try to **expand** on our project.

- **Week 1:**  
  Our focus will be on finalizing the project idea, choosing a weather API, and building a small prototype that successfully fetches and prints weather data for a test city. During this time, we will also sketch out the initial version of our weather interpretation rules and decide on the overall structure of our Python files and functions.

- **Week 2:**  
  We intend to complete the core version of the weather interpretation and packing logic modules. Our goal for this phase is to be able to pass mock or real weather data into the packing logic and receive a reasonable draft packing list in return. We will also begin implementing and connecting the command-line interface so that, by the end of the second week, there is a preliminary end-to-end flow, even if it is not yet polished.

- **Week 3:**  
  This week will be dedicated to solidifying the **MVP**. We will refine the logic, improve the structure and clarity of the CLI prompts and outputs, and start writing systematic tests for the main functionality. Our aim is that by the end of this week, we have a reliable CLI application that meets the minimum requirements: destination and date input, weather fetching, and a basic packing list output.

- **Week 4:**  
  If everything goes according to plan, the fourth week will be used to implement **stretch goals**, starting with the most feasible and impactful ones. We will likely start with a simple PDF export feature, since that builds on the existing packing list logic, and then move on to more advanced features like outfit recommendations if time permits.

- **Week 5:**  
  In the fifth and final week, we will focus on **testing, debugging, documentation**, and preparing whatever demonstration or presentation is required. We will also use this final week to clean up our repository, ensure our code is well commented, and confirm that the program runs correctly on a clean environment.

---

## 5. Collaboration Plan

As Thomas and Astrid are already friends, clear communication and division of labor should not be a problem. We plan to collaborate closely but still maintain some **specialization** so that we can work in parallel. At a high level:

- One of us will take primary responsibility for **external integration and user interaction**  
- The other will focus more on the **internal decision-making logic**

However, we will both review each other’s code and be familiar with all parts of the project to avoid single points of failure. We will meet **in person at least twice per week** and communicate effectively using **WeChat calls and direct messages**.

We will use **GitHub** as our central collaboration tool. Our workflow will involve:

- A `main` branch that is kept stable  
- A small number of **feature branches** for new functionality  

Each of us will:

1. Develop on our own feature branch  
2. Open pull requests when we are ready to merge changes into the shared codebase  
3. Have the other team member review the changes, leave comments if needed, and test the new code  

This will help maintain code quality and ensure that both of us understand how the project is evolving.

When we encounter more complex challenges, such as designing the packing rules or resolving tricky bugs, we will use **pair programming** sessions so that we can think through the problem together. Our general development approach will be **iterative and somewhat agile**: we will aim to build small, working increments of functionality and refine them through feedback and testing, rather than trying to design everything perfectly up front.

---

## 6. Risks and Limitations

We do expect several potential risks and limitations that could affect the success of this project.

One major risk is related to the **weather API** itself. The API we choose might have:

- Rate limits  
- Regional coverage gaps  
- Occasional downtime  

All of these could affect our ability to consistently fetch accurate weather data. To mitigate this, we plan to choose an API with **clear documentation**, test it early, and design our code to handle errors gracefully, including giving users informative messages if data cannot be retrieved.

Another significant risk is the **complexity of the packing logic**. It is tempting to keep adding more conditions and special cases (for example, different categories for formal events, outdoor sports, or travel with children), which could quickly make the code harder to manage and test. We intend to control this risk by clearly defining a **manageable scope for the MVP** and only expanding the rules once that MVP is solid. We will focus first on a **general-purpose traveler** and a limited set of activity types, then consider additional nuances only if time allows.

Time constraints themselves are also a limitation. Because we are only two people and have other coursework, there is a real possibility that we will not be able to implement all of the stretch goals, especially the more advanced ones like outfit generation or a polished PDF layout. To address this, we are deliberately planning to complete the MVP relatively early, so that any **stretch features** are truly optional and do not jeopardize the core functionality.

Finally, there is always the possibility of **unexpected bugs or integration issues**, particularly around date handling and user input validation. We will mitigate this by:

- Testing with a variety of scenarios  
- Building in validation checks for inputs before making API requests  

---

## 7. Additional Course Content

There are several topics from the course, or closely related to it, that would be particularly helpful for this project.

Additional examples of working with **external APIs in Python**, especially those that
involve parsing nested JSON and handling different types of errors, would reinforce what we need to do for the weather integration. Guidance on **organizing larger Python programs** into multiple files and modules in a clean, maintainable way would also support our efforts to structure the project well.

It would also be useful to see more about **basic testing strategies** for Python programs of this size. For instance, short demonstrations of how to write and run simple unit tests or how to separate logic from input/output to make testing easier would help us ensure our packing rules behave as expected.

Also, we would like to learn more about **web design and basic front-end concepts**, especially how to present our Python logic through a simple but polished web interface using tools like Flask with HTML/CSS templates. Understanding how to structure routes and templates, separate logic from presentation, and apply basic layout and UX patterns would help make our MVP more intuitive, visually appealing, and user-friendly.

We also want to improve our ability to **build clean, user-friendly input forms and outputs**. Learning how to design minimal input fields (destination, dates, trip type), validate user errors gracefully, and format the final packing recommendations in a clear, organized layout—possibly with icons, grouped sections, or small visual cues—would make the tool easier to use and feel more like a real product.

Finally, if time permits in the course, a brief introduction or pointer to libraries for tasks like **PDF generation** or lightweight web development (such as **Flask**) would give us more confidence in attempting our stretch goals. Even high-level guidance on when to use such tools and common pitfalls to avoid would be valuable as we move from a simple script toward something that feels more like a real application.

