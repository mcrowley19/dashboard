import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js'
import { PMREMGenerator } from 'three'
import { LANDING_ASSET } from '../../config/landingAsset'

const GRAY_50 = 0xf9fafb

const DURATION = 0.72
const EASE_OUT_CUBIC = (t: number) => 1 - (1 - t) * (1 - t) * (1 - t)
const EASE_OUT_BACK = (t: number) => {
  const c1 = 1.2
  const c3 = c1 + 1
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2)
}

const START_Y = 1.5
const END_Y = 0
const END_X = 0.95
const ROT_Z = 0.18
const ROT_X = -0.22
const TARGET_SIZE = 1.4  // reduced from 1.8

// Continuous spin speed (radians per second)
const SPIN_SPEED = 0.45

function createCapsule(_envMap?: THREE.Texture): THREE.Mesh {
  const geometry = new THREE.CapsuleGeometry(0.5, 1.2, 24, 48)
  const material = new THREE.ShaderMaterial({
    transparent: true,
    uniforms: {
      uOpacity: { value: 1 },
      uLightDir: { value: new THREE.Vector3(0.35, 0.6, 0.7).normalize() },
      uLight2Dir: { value: new THREE.Vector3(-0.4, 0.3, 0.5).normalize() },
      uAmbient: { value: 0.28 },
      uDiffuse: { value: 0.52 },
      uSpecular: { value: 0.35 },
      uShininess: { value: 48.0 },
      uEnvIntensity: { value: 0.42 },
      uFresnelPower: { value: 2.6 },
      uRimColor: { value: new THREE.Vector3(0.92, 0.92, 0.96) },
    },
    vertexShader: `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec3 vWorldPosition;
      varying vec3 vWorldNormal;
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vec4 worldPos = modelMatrix * vec4(position, 1.0);
        vWorldPosition = worldPos.xyz;
        vWorldNormal = normalize((modelMatrix * vec4(normal, 0.0)).xyz);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform float uOpacity;
      uniform vec3 uLightDir;
      uniform vec3 uLight2Dir;
      uniform float uAmbient;
      uniform float uDiffuse;
      uniform float uSpecular;
      uniform float uShininess;
      uniform float uEnvIntensity;
      uniform float uFresnelPower;
      uniform vec3 uRimColor;
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec3 vWorldPosition;
      varying vec3 vWorldNormal;

      void main() {
        vec3 red = vec3(0.937, 0.267, 0.267);
        vec3 white = vec3(1.0, 1.0, 1.0);
        vec3 baseCol = vPosition.y >= 0.0 ? red : white;

        vec3 N = normalize(vWorldNormal);
        vec3 V = normalize(cameraPosition - vWorldPosition);

        float NdotL = max(0.0, dot(N, normalize(uLightDir)));
        float NdotL2 = max(0.0, dot(N, normalize(uLight2Dir)));
        float diffuse = uAmbient + uDiffuse * (NdotL + 0.4 * NdotL2);
        vec3 lit = baseCol * diffuse;

        vec3 H = normalize(normalize(uLightDir) + V);
        float NdotH = max(0.0, dot(N, H));
        float spec = pow(NdotH, uShininess);
        lit += vec3(1.0, 1.0, 1.0) * uSpecular * spec;

        float NdotV = max(0.0, dot(N, V));
        float fresnel = pow(1.0 - NdotV, uFresnelPower);
        vec3 reflectDir = reflect(-V, N);
        float y = reflectDir.y;
        vec3 envCol = vec3(0.52 + 0.22 * y, 0.55 + 0.22 * y, 0.62 + 0.18 * y);
        lit = mix(lit, lit + envCol * uEnvIntensity, fresnel);
        lit = mix(lit, uRimColor, fresnel * 0.25);

        gl_FragColor = vec4(lit, uOpacity);
      }
    `,
  })
  const mesh = new THREE.Mesh(geometry, material)
  mesh.scale.setScalar(0.975)
  mesh.castShadow = true
  mesh.receiveShadow = true
  return mesh
}

function normalizeModelSize(obj: THREE.Object3D, targetSize: number): void {
  const box = new THREE.Box3().setFromObject(obj)
  const size = new THREE.Vector3()
  box.getSize(size)
  const maxDim = Math.max(size.x, size.y, size.z)
  if (maxDim <= 0) return
  const s = targetSize / maxDim
  obj.scale.setScalar(s)
}

function setMaterialsOpacity(obj: THREE.Object3D, opacity: number): void {
  obj.traverse((child) => {
    if (child instanceof THREE.Mesh && child.material) {
      const mat = child.material as THREE.Material & { opacity?: number; transparent?: boolean }
      mat.transparent = true
      mat.opacity = opacity
    }
  })
}

export default function LandingScene() {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<{
    renderer: THREE.WebGLRenderer
    frameId: number
  } | null>(null)

  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    const width = container.clientWidth
    const height = container.clientHeight

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(GRAY_50)
    scene.fog = new THREE.Fog(GRAY_50, 8, 22)

    const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100)
    camera.position.set(0, 0, 4.8)
    camera.lookAt(0, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false })
    renderer.setSize(width, height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    renderer.toneMapping = THREE.ACESFilmicToneMapping
    renderer.toneMappingExposure = 1.0
    renderer.outputColorSpace = THREE.SRGBColorSpace
    container.appendChild(renderer.domElement)

    const roomEnv = new RoomEnvironment()
    const pmremGenerator = new PMREMGenerator(renderer)
    const envMap = pmremGenerator.fromScene(roomEnv).texture
    scene.environment = envMap
    roomEnv.dispose()
    pmremGenerator.dispose()

    const groundGeometry = new THREE.PlaneGeometry(20, 20)
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0xf0f1f3,
      roughness: 0.9,
      metalness: 0,
    })
    const ground = new THREE.Mesh(groundGeometry, groundMaterial)
    ground.rotation.x = -Math.PI / 2
    ground.position.y = -2.2
    ground.receiveShadow = true
    scene.add(ground)

    const group = new THREE.Group()
    group.position.set(END_X, START_Y, 0)
    group.rotation.order = 'YXZ'
    group.rotation.z = ROT_Z
    group.rotation.x = ROT_X
    scene.add(group)

    let capsule: THREE.Mesh | null = createCapsule(envMap)
    let modelRoot: THREE.Object3D | null = null
    let capsuleMat: THREE.ShaderMaterial | null = (capsule.material as THREE.ShaderMaterial)
    group.add(capsule)

    const loader = new GLTFLoader()
    const modelUrl = LANDING_ASSET.modelUrl

    loader.load(
      modelUrl,
      (gltf) => {
        if (!containerRef.current) return
        const root = gltf.scene
        normalizeModelSize(root, TARGET_SIZE)
        setMaterialsOpacity(root, 0)
        root.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.castShadow = true
            child.receiveShadow = true
            const mat = child.material as THREE.MeshStandardMaterial
            if (mat && mat.isMeshStandardMaterial) mat.envMapIntensity = 1.0
          }
        })
        if (capsule) {
          group.remove(capsule)
          capsule = null
          capsuleMat = null
        }
        modelRoot = root
        group.add(root)
      },
      undefined,
      () => {
        if (!capsule && group.children.length === 0) {
          capsule = createCapsule(envMap)
          capsuleMat = capsule.material as THREE.ShaderMaterial
          group.add(capsule)
        }
      }
    )

    const ambient = new THREE.AmbientLight(0xffffff, 0.26)
    scene.add(ambient)

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.05)
    keyLight.position.set(4, 5, 6)
    keyLight.castShadow = true
    keyLight.shadow.mapSize.set(2048, 2048)
    keyLight.shadow.camera.near = 0.5
    keyLight.shadow.camera.far = 25
    keyLight.shadow.camera.left = -6
    keyLight.shadow.camera.right = 6
    keyLight.shadow.camera.top = 6
    keyLight.shadow.camera.bottom = -6
    keyLight.shadow.bias = -0.0001
    keyLight.shadow.normalBias = 0.02
    scene.add(keyLight)

    const fillLight = new THREE.DirectionalLight(0xe8ecf4, 0.48)
    fillLight.position.set(-4, 2, 3)
    scene.add(fillLight)

    const rimLight = new THREE.DirectionalLight(0xffffff, 0.38)
    rimLight.position.set(0, 3, -5)
    scene.add(rimLight)

    const startTime = Date.now()
    let frameId = 0

    function animate() {
      frameId = requestAnimationFrame(animate)
      const elapsed = (Date.now() - startTime) * 0.001

      // Drop-in
      const t = Math.min(1, elapsed / DURATION)
      group.position.y = START_Y + (END_Y - START_Y) * EASE_OUT_BACK(t)
      group.scale.setScalar(0.96 + 0.04 * EASE_OUT_CUBIC(t))

      // Fade in
      const fade = EASE_OUT_CUBIC(t)
      if (capsuleMat) capsuleMat.uniforms.uOpacity.value = fade
      if (modelRoot) setMaterialsOpacity(modelRoot, fade)

      // Constant Y spin — eases in with the fade so start isn't abrupt
      group.rotation.y = elapsed * SPIN_SPEED * Math.min(1, fade * 2)
      group.rotation.x = ROT_X
      group.rotation.z = ROT_Z

      renderer.render(scene, camera)
    }
    animate()

    sceneRef.current = { renderer, frameId }

    const onResize = () => {
      if (!containerRef.current) return
      const w = containerRef.current.clientWidth
      const h = containerRef.current.clientHeight
      camera.aspect = w / h
      camera.updateProjectionMatrix()
      renderer.setSize(w, h)
    }
    window.addEventListener('resize', onResize)

    return () => {
      window.removeEventListener('resize', onResize)
      cancelAnimationFrame(frameId)
      envMap.dispose()
      renderer.dispose()
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement)
      }
      sceneRef.current = null
    }
  }, [])

  return <div ref={containerRef} className="absolute inset-0 w-full h-full" aria-hidden />
}