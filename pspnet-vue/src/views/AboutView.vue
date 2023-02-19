<template>
  <div class="main-grid">
    <nav class="flex justify-start h-screen bg-[#b9e0a5]">
      <ul class="nav-rail-ul sticky">
        <li><a href="#psProperty">Plant and Soil Property Classification</a></li>
        <li><a href="#background">Background</a></li>
        <li><a href="#goals">Goals</a></li>
        <li><a href="#dataset">Dataset</a></li>
        <li><a href="#research">Research</a></li>
        <li><a href="#resources">Resources</a></li>
      </ul>
    </nav>
    <div class="right-side">
      <div>
          <h1 class="about-section" id="psProperty">Plant and Soil Property Classification Network</h1>
          <p class="about-paragraph">The PSPNet project builds the foundational machine learning tools and architecture, interfaced using a web application. The larger project’s goals are to present new benchmark datasets for plant and soil properties and their effects on wildfire dynamics, and to use state of the art machine learning models to address the wildfire problem domain. Currently, our project has developed a small example dataset containing 99 images total in order to train YOLOv5 and Facebook’s Detectron2 machine learning model. Furthermore, we developed a website demonstrating the different functionalities of our website to address plant classification: user-related pages, an image dataset gallery page, and an image classification page.</p>
      </div>
      <div>
          <br>
          <h1 class="about-section" id="background">Background</h1>
          <p class="about-paragraph">As a result of wildfires in the U.S., Burned Area Emergency Response (BAER) teams are deployed to assess post-fire burn severity to protect humans and their resources. One important aspect of this assessment is the rapid development of a post-burn severity map. This map allows BAER teams to quickly assess the fire's effects on plant and soil properties in the region. The main species of concern for wildfires in Nevada is sagebrush. In conjunction with dry soil and weather, sagebrush fires can reach up to 30 feet and burn thousands of acres, threatening the livelihood of some Nevadans. As scientists devise strategies to identify areas of concern, there develops a need for a tool which rapidly identifies plant and soil properties to create a post-burn severity map. Thus, PSPNet will provide 2 major contributions: (1) provide experimental results of plant image classification using deep learning models with transfer learning, and (2) provide a web interface which includes a labeling tool, access to the trained models, and a user contribution system.</p>
          <p class="about-paragraph">The first contribution is largely inspired by the works of Pl@ntNet, a machine learning tool designed for plant image classification. PSPNet will improve upon Pl@ntNet, aiming to achieve better results on the Pl@ntNet-300K dataset. This dataset consists of over 300,000 plant images and over 1000 species. Our team will train several deep learning models and report the results on the web interface. Also, PSPNet will develop models for plant and soil burn severity mapping. The image dataset for burn severity properties will not be large, thus requiring transfer learning to produce these models.</p>
          <p class="about-paragraph">For the second contribution, our team will embed the models into the web interface, allowing users to classify their images. Users will be able to contribute labeled images to the dataset. The overarching goal of this project is to provide future developers the foundational architecture necessary to quickly continue developing the machine learning aspect of the project for the domain experts and others to use.</p>
          <p class="about-paragraph">The team has developed the software for our models and front-end. Currently, we have a functional front-end with several web pages following our reported designs. We have trained two deep learning models: YOLOv5 and Detectron2. One major functional requirement was added since the last project report: we will use transfer learning to develop models for identifying burn severity properties using a smaller dataset.</p>
      </div>
      <div>
          <br>
          <h1 class="about-section" id="goals">Goals</h1>
          <p class="about-paragraph">The overall objectives of this prototype was to implement a functional front-end and to implement “toy” machine learning models. The specific breakdown of these objectives are described in the following section, listing out the significant items completed for each objective. The team agreed to first complete a functional front-end for two reasons: (1) the team can focus on learning, implementing, and connecting a back-end; and (2) the team wanted to take this opportunity to learn web development from the beginning. After demonstrating the prototype, the team was alerted of better practices for web development which is discussed further in Section 5. With the front end, the team agreed to complete the implementation and training of a couple “toy” machine learning models for two reasons: (1) to demonstrate what models may output, and (2) to have models to later connect to the front end. The models were trained on a small dataset of plant images to lessen the time cost spent which resulted in varying levels of success in detecting sagebrush in the images. The team intends to later retrain these models,and implement and test other models on a larger dataset.</p>
      </div>
      <div>
          <br>
          <h1 class="about-section" id="dataset">Dataset</h1>
          <p class="about-paragraph">The current data set used to train our models is the Pl@ntNet-300K data set. In the future, we are hoping to receive the specific data set to the wildfire research project. However, gathering the data is a labor and time insensive project and likely will not be completed in time to train on.</p>
      </div>
      <div>
          <br>
          <h1 class="about-section" id="research">Research</h1>
          <p class="about-paragraph">Related research includes the <a href="https://plantnet.org/en/">Pl@ntNet</a> research project. This aimed to create a model which is able to classify a plant species within a given photo.</p>
      </div>
      <div>
          <br>
          <h1 class="about-section" id="resources">Resources</h1>
          <p class="about-paragraph">If you would like to learn more, check out these resources:</p>
          <ul>
            <li>
              <a href="https://www.unr.edu/nevada-today/news/2022/20m-dollar-fire-science-project">NSHE Awarded $20 million National Science Foundation research award for fire science</a>
            </li>
            <li>
              <a href="https://www.cse.unr.edu/~lyang/">Project advisor Dr. Lei Yang</a>
            </li>
          </ul>
      </div>
    </div>
  </div>
</template>

<script>

</script>

<style>
  .main-grid {
      display: grid;
      grid-template-columns: 140px 9fr 1fr;
      position: absolute;
  }
  .right-side {
    padding: 20px;
    justify-items: left;
    max-height: 50%;
    overflow-y: scroll;
    margin: 30px;
    margin-right: 0px;
  }
  .nav-links {
   display: inline;
  }
  .about-section {
    font-size:x-large;
  }
  .about-paragraph {
    text-align: left;
    text-indent: 5%;
  }
  .nav-rail-ul li {
    margin-top: 2px;
    margin-bottom: 20px
  }
</style>