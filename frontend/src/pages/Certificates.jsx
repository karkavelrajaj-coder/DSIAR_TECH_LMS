import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Certificates() {
  const [certs, setCerts] = useState([]);
  const [images, setImages] = useState({}); // cert_id -> object URL
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let objectUrls = [];

    api.get("/certificates").then(async (res) => {
      setCerts(res.data);
      setLoading(false);

      // A plain <img src="..."> can't carry the Authorization header, so
      // fetch each certificate PNG through axios (which does attach it)
      // and turn the response into an object URL the <img> tag can use.
      for (const cert of res.data) {
        try {
          const imgRes = await api.get(`/certificates/${cert.cert_id}/image`, {
            responseType: "blob",
          });
          const url = URL.createObjectURL(imgRes.data);
          objectUrls.push(url);
          setImages((prev) => ({ ...prev, [cert.cert_id]: url }));
        } catch {
          // leave it unset; the UI just won't show that one image
        }
      }
    });

    return () => objectUrls.forEach((u) => URL.revokeObjectURL(u));
  }, []);

  if (loading) return <div className="text-gray-500">Loading…</div>;

  if (certs.length === 0) {
    return (
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">🏆 My certificates</h1>
        <div className="mt-6 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-700">
          No certificates yet. A certificate is issued automatically once
          you've completed every lesson in a course AND your assignment has
          been approved.
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">🏆 My certificates</h1>
      <div className="mt-6 space-y-6">
        {certs.map((cert) => (
          <div key={cert.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">🎓 {cert.course_title}</h2>
            <div className="text-xs text-gray-500">
              Certificate ID: {cert.cert_id} · Issued{" "}
              {new Date(cert.issued_at).toLocaleDateString(undefined, {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </div>
            {images[cert.cert_id] ? (
              <>
                <img
                  src={images[cert.cert_id]}
                  alt={`Certificate for ${cert.course_title}`}
                  className="mt-3 w-full rounded-lg border"
                />
                <a
                  href={images[cert.cert_id]}
                  download={`dsiar-certificate-${cert.course_title.replace(/\s+/g, "_")}.png`}
                  className="mt-3 inline-block rounded-lg bg-purple-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-purple-700"
                >
                  Download certificate (PNG)
                </a>
              </>
            ) : (
              <div className="mt-3 text-sm text-gray-400">Loading certificate image…</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
