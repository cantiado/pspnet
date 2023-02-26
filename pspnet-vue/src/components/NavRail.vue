<!-- Author: Antonio Lang -->

<template>
    <div class="nav-rail">
        <nav class="nav-links">
            <ul class="nav-rail-ul">
                <li><a href="#psProperty">Plant and Soil Property Classification</a></li>
                <li><a href="#background">Background</a></li>
                <li><a href="#goals">Goals</a></li>
                <li><a href="#dataset">Dataset</a></li>
                <li><a href="#research">Research</a></li>
                <li><a href="#resources">Resources</a></li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
  setup(){
    let name = 'NavRail'
    return {name}
  }
}
</script>

<style>
    .nav-rail {
        background-color: #b9e0a5ff;
        height: 100%;
    }
    .nav-links {
        justify-items: left;
    }
    .nav-rail li {
        margin-bottom: 20px;
        color: black;
    }
</style>