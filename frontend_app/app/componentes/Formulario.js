'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { useState } from 'react'

const formSchema = z.object({
  titulo: z.string().min(5, 'El título debe tener al menos 5 caracteres').max(100, 'El título no puede exceder los 100 caracteres'),
  texto: z.string().min(20, 'El texto debe tener al menos 20 caracteres').max(1000, 'El texto no puede exceder los 1000 caracteres'),
})

export default function FormularioContacto() {
  const [isSuccess, setIsSuccess] = useState(false);
  const [responseData, setResponseData] = useState(null); 
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      titulo: '',
      texto: '',
    },
  });

  const onSubmit = async (data) => {
    
    setIsSuccess(false);
    setResponseData(null); 

    try {
      console.log('Datos enviados:', data);
      await new Promise((resolve) => setTimeout(resolve, 500)); 
      
      const payload = {
        title: data.titulo,
        content: data.texto,
      };
      
      const response = await fetch('http://localhost:8001/documents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al enviar el formulario');
      }
      
      const result = await response.json(); 
      setResponseData(result); 
      setIsSuccess(true);
      reset();
      
      
    } catch (error) {
      console.error('Error al enviar el formulario:', error);
     
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Predecir categoria</h2>
        <p className="text-gray-600">
          Complete los campos para predecir la categoria de acuerdo con la solicitud.
        </p>
      </div>
      
      {isSuccess && responseData && (
        <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          <p>¡Contenido enviado con éxito!</p>
          <p className="font-bold">Categoría Predicha: {responseData.category}</p> 
          <p className="text-sm text-gray-600">ID: {responseData.id}</p>
          <p className="text-sm text-gray-600">Título: {responseData.title}</p>
          
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
    
        <div>
          <label htmlFor="titulo" className="block text-sm font-medium text-gray-700 mb-1">
            Título *
          </label>
          <input
            id="titulo"
            type="text"
            {...register('titulo')}
            className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
              errors.titulo
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
            }`}
            placeholder="Ingrese el título aquí"
          />
          {errors.titulo && (
            <p className="mt-1 text-sm text-red-600">{errors.titulo.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="texto" className="block text-sm font-medium text-gray-700 mb-1">
            Texto *
          </label>
          <textarea
            id="texto"
            rows={8} 
            {...register('texto')}
            className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
              errors.texto
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
            }`}
            placeholder="Escriba el contenido de su texto aquí..."
          />
          {errors.texto && (
            <p className="mt-1 text-sm text-red-600">{errors.texto.message}</p>
          )}
        </div>

        
        <div className="pt-2">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full py-3 px-4 rounded-md shadow-sm text-white font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors ${
              isSubmitting
                ? 'bg-blue-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
            }`}
          >
            {isSubmitting ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Enviando...
              </span>
            ) : (
              'Enviar Contenido'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}