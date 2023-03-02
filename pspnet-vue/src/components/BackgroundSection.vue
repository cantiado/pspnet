<template>
  <h1 class="text-3xl mb-5">Background</h1>
  <p>
    As a result of wildfires in the U.S., Burned Area Emergency Response (BAER)
    teams are deployed to assess post-fire burn severity to protect humans and
    their resources. One important aspect of this assessment is the rapid
    development of a post-burn severity map. This map allows BAER teams to
    quickly assess the fire's effects on plant and soil properties in the
    region. The main species of concern for wildfires in Nevada is sagebrush. In
    conjunction with dry soil and weather, sagebrush fires can reach up to 30
    feet and burn thousands of acres, threatening the livelihood of some
    Nevadans. As scientists devise strategies to identify areas of concern,
    there develops a need for a tool which rapidly identifies plant and soil
    properties to create a post-burn severity map. Thus, PSPNet will provide 2
    major contributions: (1) provide experimental results of plant image
    classification using deep learning models with transfer learning, and (2)
    provide a web interface which includes a labeling tool, access to the
    trained models, and a user contribution system.
  </p>
  <p>
    The first contribution is largely inspired by the works of Pl@ntNet, a
    machine learning tool designed for plant image classification. PSPNet will
    improve upon Pl@ntNet, aiming to achieve better results on the Pl@ntNet-300K
    dataset. This dataset consists of over 300,000 plant images and over 1000
    species. Our team will train several deep learning models and report the
    results on the web interface. Also, PSPNet will develop models for plant and
    soil burn severity mapping. The image dataset for burn severity properties
    will not be large, thus requiring transfer learning to produce these models.
  </p>
  <p>
    For the second contribution, our team will embed the models into the web
    interface, allowing users to classify their images. Users will be able to
    contribute labeled images to the dataset. The overarching goal of this
    project is to provide future developers the foundational architecture
    necessary to quickly continue developing the machine learning aspect of the
    project for the domain experts and others to use.
  </p>
  <p>
    The team has developed the software for our models and front-end. Currently,
    we have a functional front-end with several web pages following our reported
    designs. We have trained two deep learning models: YOLOv5 and Detectron2.
    One major functional requirement was added since the last project report: we
    will use transfer learning to develop models for identifying burn severity
    properties using a smaller dataset.
  </p>
</template>
