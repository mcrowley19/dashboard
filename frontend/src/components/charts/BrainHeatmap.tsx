import { useEffect, useRef } from 'react'

export default function BrainHeatmap() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    const w = canvas.width
    const h = canvas.height

    ctx.clearRect(0, 0, w, h)

    const drawHeatBlob = (cx: number, cy: number, rx: number, ry: number, color: string, alpha: number) => {
      const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(rx, ry))
      gradient.addColorStop(0, color.replace(')', `,${alpha})`).replace('rgb', 'rgba'))
      gradient.addColorStop(0.5, color.replace(')', `,${alpha * 0.5})`).replace('rgb', 'rgba'))
      gradient.addColorStop(1, 'rgba(0,0,0,0)')
      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2)
      ctx.fill()
    }

    // Brain outline shape
    ctx.save()
    ctx.globalAlpha = 0.15
    ctx.fillStyle = '#4a6'
    ctx.beginPath()
    ctx.ellipse(w / 2, h / 2 - 10, w * 0.38, h * 0.42, 0, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()

    // Midline
    ctx.strokeStyle = 'rgba(100,200,100,0.1)'
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.moveTo(w / 2, h * 0.08)
    ctx.lineTo(w / 2, h * 0.88)
    ctx.stroke()

    // Green base layer
    drawHeatBlob(w * 0.5, h * 0.45, w * 0.35, h * 0.38, 'rgb(30,120,50)', 0.4)

    // Frontal regions
    drawHeatBlob(w * 0.42, h * 0.25, w * 0.12, h * 0.1, 'rgb(80,180,60)', 0.5)
    drawHeatBlob(w * 0.58, h * 0.25, w * 0.12, h * 0.1, 'rgb(80,180,60)', 0.5)

    // Central hot spots
    drawHeatBlob(w * 0.38, h * 0.42, w * 0.1, h * 0.12, 'rgb(220,200,30)', 0.6)
    drawHeatBlob(w * 0.62, h * 0.42, w * 0.1, h * 0.12, 'rgb(220,200,30)', 0.6)

    // Hot center areas
    drawHeatBlob(w * 0.45, h * 0.5, w * 0.08, h * 0.09, 'rgb(240,140,20)', 0.7)
    drawHeatBlob(w * 0.55, h * 0.5, w * 0.08, h * 0.09, 'rgb(240,140,20)', 0.7)

    // Peak red spots
    drawHeatBlob(w * 0.42, h * 0.55, w * 0.06, h * 0.06, 'rgb(220,50,20)', 0.65)
    drawHeatBlob(w * 0.58, h * 0.55, w * 0.06, h * 0.06, 'rgb(220,50,20)', 0.65)

    // Posterior regions
    drawHeatBlob(w * 0.5, h * 0.65, w * 0.14, h * 0.12, 'rgb(200,160,20)', 0.5)
    drawHeatBlob(w * 0.38, h * 0.62, w * 0.08, h * 0.08, 'rgb(240,120,20)', 0.5)
    drawHeatBlob(w * 0.62, h * 0.62, w * 0.08, h * 0.08, 'rgb(240,120,20)', 0.5)

    // Temporal lobes
    drawHeatBlob(w * 0.25, h * 0.48, w * 0.08, h * 0.12, 'rgb(60,160,50)', 0.4)
    drawHeatBlob(w * 0.75, h * 0.48, w * 0.08, h * 0.12, 'rgb(60,160,50)', 0.4)

    // Occipital
    drawHeatBlob(w * 0.5, h * 0.75, w * 0.1, h * 0.08, 'rgb(100,180,60)', 0.4)

    // Scattered green peripheral
    drawHeatBlob(w * 0.3, h * 0.3, w * 0.06, h * 0.08, 'rgb(40,140,40)', 0.3)
    drawHeatBlob(w * 0.7, h * 0.3, w * 0.06, h * 0.08, 'rgb(40,140,40)', 0.3)
  }, [])

  return <canvas ref={canvasRef} width={500} height={400} className="w-full h-full" />
}
