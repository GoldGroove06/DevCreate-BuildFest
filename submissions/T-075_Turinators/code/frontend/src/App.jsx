import { useState } from "react"
import { Toast } from "./components/Toast"

const UploadLogo = () => (<svg width="75" height="75" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.81825 1.18188C7.64251 1.00615 7.35759 1.00615 7.18185 1.18188L4.18185 4.18188C4.00611 4.35762 4.00611 4.64254 4.18185 4.81828C4.35759 4.99401 4.64251 4.99401 4.81825 4.81828L7.05005 2.58648V9.49996C7.05005 9.74849 7.25152 9.94996 7.50005 9.94996C7.74858 9.94996 7.95005 9.74849 7.95005 9.49996V2.58648L10.1819 4.81828C10.3576 4.99401 10.6425 4.99401 10.8182 4.81828C10.994 4.64254 10.994 4.35762 10.8182 4.18188L7.81825 1.18188ZM2.5 9.99997C2.77614 9.99997 3 10.2238 3 10.5V12C3 12.5538 3.44565 13 3.99635 13H11.0012C11.5529 13 12 12.5528 12 12V10.5C12 10.2238 12.2239 9.99997 12.5 9.99997C12.7761 9.99997 13 10.2238 13 10.5V12C13 13.104 12.1062 14 11.0012 14H3.99635C2.89019 14 2 13.103 2 12V10.5C2 10.2238 2.22386 9.99997 2.5 9.99997Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path></svg>)
function App() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState(null)
  const [output, setOutput] = useState(null)
  const [loading, setLoading] = useState(false)
  const [toasts, setToasts] = useState([]);

  const showToast = (msg) => {
    const id = Date.now();
    const newToast = (
      <Toast
        key={id}
        message={msg}
        duration={3000}
        onClose={() => setToasts((prev) => prev.filter((t) => t.key !== id))}
      />
    );
    setToasts((prev) => [...prev, newToast]);
  };

  const handleUpload = async () => {
    if (!file) {
      showToast(<div>Please select a file</div>)
      return
    }
    setLoading(true)

    const formData = new FormData();
    formData.append("video", file);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log(data)
    setOutput(data.url);
    setLoading(false);
  }
  return (
    <div className="bg-white text-black w-full h-screen flex flex-col  items-center my-8">
      {toasts.map((toast) => toast)}
      <div className="bg-gray-200 rounded-xl w-[400px] h-[200px] flex items-center justify-center mb-8 flex-col flex">
        {loading ? "loading" : (<>
          <UploadLogo />
          <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button onClick={handleUpload} className="bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded mt-4">Start Processing</button>

        </>)}
      </div>
      {file && (
       
          <div>
            <video width="420" height="240" controls preload="metadata">
              <source src={URL.createObjectURL(file)} type="video/mp4" />
            </video>
          </div>
      )}
      {output && (<div>

        <div>Video successfully processed</div>
        <a href={output} download="output.mp4" className="bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded mt-8">Download</a>
      </div>
      )}
    </div>
  )
}

export default App
