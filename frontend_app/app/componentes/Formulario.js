// components/FormularioContacto.jsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { useState } from 'react'

// Esquema de validación con Zod
const formSchema = z.object({
  nombre: z.string().min(2, 'Mínimo 2 caracteres').max(50),
  email: z.string().email('Ingrese un email válido'),
  telefono: z.string().regex(/^[0-9]+$/, 'Solo números').optional(),
  asunto: z.string().min(3, 'Mínimo 3 caracteres').max(100),
  mensaje: z.string().min(10, 'Mínimo 10 caracteres').max(500),
  terminos: z.literal(true, {
    errorMap: () => ({ message: 'Debe aceptar los términos y condiciones' }),
  }),
})

export default function FormularioContacto() {
  const [isSuccess, setIsSuccess] = useState(false)
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nombre: '',
      email: '',
      telefono: '',
      asunto: '',
      mensaje: '',
      terminos: false,
    },
  })

  const onSubmit = async (data) => {
    try {
      // Simulación de envío a API
      console.log('Datos enviados:', data)
      await new Promise((resolve) => setTimeout(resolve, 1500))
      
      // En producción, reemplazar con:
      // const response = await fetch('/api/contacto', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(data),
      // })
      
      setIsSuccess(true)
      reset()
      
      // Ocultar mensaje de éxito después de 5 segundos
      setTimeout(() => setIsSuccess(false), 5000)
    } catch (error) {
      console.error('Error al enviar el formulario:', error)
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Contáctenos</h2>
        <p className="text-gray-600">
          Complete el formulario y nuestro equipo se comunicará con usted a la brevedad.
        </p>
      </div>
      
      {isSuccess && (
        <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          <p>¡Formulario enviado con éxito! Nos pondremos en contacto pronto.</p>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Campo Nombre */}
          <div>
            <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 mb-1">
              Nombre Completo *
            </label>
            <input
              id="nombre"
              type="text"
              {...register('nombre')}
              className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
                errors.nombre
                  ? 'border-red-500 focus:ring-red-200'
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
              }`}
              placeholder="Juan Pérez"
            />
            {errors.nombre && (
              <p className="mt-1 text-sm text-red-600">{errors.nombre.message}</p>
            )}
          </div>

          {/* Campo Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Correo Electrónico *
            </label>
            <input
              id="email"
              type="email"
              {...register('email')}
              className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
                errors.email
                  ? 'border-red-500 focus:ring-red-200'
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
              }`}
              placeholder="juan@ejemplo.com"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>
        </div>

        {/* Campo Teléfono */}
        <div>
          <label htmlFor="telefono" className="block text-sm font-medium text-gray-700 mb-1">
            Teléfono
          </label>
          <input
            id="telefono"
            type="tel"
            {...register('telefono')}
            className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
              errors.telefono
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
            }`}
            placeholder="+54 11 1234 5678"
          />
          {errors.telefono && (
            <p className="mt-1 text-sm text-red-600">{errors.telefono.message}</p>
          )}
        </div>

        {/* Campo Asunto */}
        <div>
          <label htmlFor="asunto" className="block text-sm font-medium text-gray-700 mb-1">
            Asunto *
          </label>
          <input
            id="asunto"
            type="text"
            {...register('asunto')}
            className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
              errors.asunto
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
            }`}
            placeholder="Motivo de su consulta"
          />
          {errors.asunto && (
            <p className="mt-1 text-sm text-red-600">{errors.asunto.message}</p>
          )}
        </div>

        {/* Campo Mensaje */}
        <div>
          <label htmlFor="mensaje" className="block text-sm font-medium text-gray-700 mb-1">
            Mensaje *
          </label>
          <textarea
            id="mensaje"
            rows={5}
            {...register('mensaje')}
            className={`w-full px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 ${
              errors.mensaje
                ? 'border-red-500 focus:ring-red-200'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
            }`}
            placeholder="Describa su consulta en detalle..."
          />
          {errors.mensaje && (
            <p className="mt-1 text-sm text-red-600">{errors.mensaje.message}</p>
          )}
        </div>

        {/* Checkbox Términos */}
        <div className="flex items-start">
          <div className="flex items-center h-5">
            <input
              id="terminos"
              type="checkbox"
              {...register('terminos')}
              className={`h-4 w-4 rounded focus:ring-blue-500 ${
                errors.terminos ? 'border-red-500 text-red-600' : 'border-gray-300 text-blue-600'
              }`}
            />
          </div>
          <div className="ml-3 text-sm">
            <label htmlFor="terminos" className="font-medium text-gray-700">
              Acepto los términos y condiciones *
            </label>
            <p className="text-gray-500">
              Al enviar este formulario, acepto la política de privacidad y el tratamiento de mis datos.
            </p>
            {errors.terminos && (
              <p className="mt-1 text-sm text-red-600">{errors.terminos.message}</p>
            )}
          </div>
        </div>

        {/* Botón de Envío */}
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
              'Enviar Mensaje'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}