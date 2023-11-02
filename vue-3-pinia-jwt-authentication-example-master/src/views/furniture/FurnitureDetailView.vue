<template>
    <div>
        <h2>Mueble {{ furniture.nombre }}</h2>
        <li>Nombre: {{ furniture.nombre }} </li>
        <li>Plazo de fabricación: {{ furniture.plazo_fabricacion }}</li>
        <li>Fecha de lanzamiento estimada: {{ furniture.fecha_lanzamiento_estimada }}</li>
        <li>Descripción: {{ furniture.descripcion }}</li>
        <li>Imagen: {{ furniture.imagen }}</li>
        <li>Plan de fabricación: {{ furniture.plan_fabricacion }}</li>
        <li>Materiales: {{ furniture.materiales }}</li>
        <li>Colección: {{ furniture.coleccion }}</li>
    </div>
</template>
