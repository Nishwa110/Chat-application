import { useState, useEffect, useRef } from "react"; 
import io from "socket.io-client";
import CryptoJS from "crypto-js";

const socket = io("http://127.0.0.1:5000");
const SECRET_KEY = "mysecretkey12345";

function ChatApp() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [windowHeight, setWindowHeight] = useState(window.innerHeight);
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);

  // ✅ Load previous chat history from localStorage on startup
  useEffect(() => {
    const savedChats = localStorage.getItem("chatHistory");
    if (savedChats) {
      setMessages(JSON.parse(savedChats));
    }
  }, []);

  // ✅ Save updated chat history to localStorage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("chatHistory", JSON.stringify(messages));
    }
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
      setWindowHeight(window.innerHeight);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    socket.on("message", (encryptedMsg) => {
      try {
        const bytes = CryptoJS.AES.decrypt(
          encryptedMsg,
          CryptoJS.enc.Utf8.parse(SECRET_KEY),
          { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }
        );
        const decryptedMsg = bytes.toString(CryptoJS.enc.Utf8);

        setMessages((prev) => [...prev, { 
          from: "bot", 
          text: decryptedMsg,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      } catch (err) {
        console.error("Decryption failed:", err);
      }
    });

    return () => socket.off("message");
  }, []);

  const sendMessage = () => {
    if (!message.trim()) return;

    const encryptedMsg = CryptoJS.AES.encrypt(
      message,
      CryptoJS.enc.Utf8.parse(SECRET_KEY),
      { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }
    ).toString();

    socket.send(encryptedMsg);

    setMessages((prev) => [...prev, { 
      from: "you",
      text: message,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);
    setMessage("");
  };

  const clearChat = () => {
    localStorage.removeItem("chatHistory");
    setMessages([]);
  };

  const getContainerStyles = () => {
    const baseTopPadding = windowHeight < 600 ? 16 : windowWidth < 480 ? 20 : 28;

    const base = {
      fontFamily: "'Poppins', sans-serif",
      boxShadow: "0 8px 32px rgba(126, 108, 142, 0.12)",
      border: "1px solid rgba(255, 255, 255, 0.8)",
      position: "relative",
      overflow: "visible",       
      boxSizing: "border-box",
      background: "linear-gradient(135deg, #f9f6fb 0%, #f0eaf8 100%)",
      borderRadius: "24px",
      paddingTop: baseTopPadding  
    };

    if (windowHeight < 600 || windowWidth < 480) {
      return { ...base, width: "calc(100vw - 30px)", margin: "15px auto", padding: "16px 12px" };
    } else if (windowWidth < 768) {
      return { ...base, width: "380px", margin: "25px auto", padding: "20px" };
    } else {
      return { ...base, width: "420px", margin: "40px auto", padding: "24px" };
    }
  };

  const getChatHeight = () => {
    if (windowHeight < 600) return "200px";
    if (windowWidth < 480) return "220px";
    if (windowWidth < 768) return "260px";
    return "300px";
  };

  const getMessageMaxWidth = () => {
    if (windowWidth < 480) return "200px";
    if (windowWidth < 768) return "240px";
    return "280px";
  };

  const getTopMargin = () => {
    if (windowHeight < 600) return "8px";
    if (windowHeight < 700) return "12px";
    return "24px";
  };

  const pastelColors = {
    primary: "linear-gradient(135deg, #ad90dcff 0%, #c8b6e2 100%)",
    secondary: "linear-gradient(135deg, #b8e2d4 0%, #a8d8c8 100%)",
    accent: "linear-gradient(135deg, #eaaebfff 0%, #f0b8ca 100%)",
    background: "linear-gradient(135deg, #f9f6fb 0%, #f0eaf8 100%)",
    yourMessage: "linear-gradient(135deg, #e8dff5 0%, #d4c4ed 100%)",
    botMessage: "linear-gradient(135deg, #dcebf1 0%, #c8e0ed 100%)",
    input: "rgba(255, 255, 255, 0.9)",
    text: "#5a4a6a"
  };

  const containerStyles = getContainerStyles();

  return (
    <div ref={containerRef} style={containerStyles}>
      <div style={{
        position: "absolute",
        top: windowHeight < 600 ? -40 : windowWidth < 480 ? -60 : -75,  
        right: windowHeight < 600 ? -30 : windowWidth < 480 ? -40 : -50,
        width: windowHeight < 600 ? 60 : windowWidth < 480 ? 80 : 100,
        height: windowHeight < 600 ? 60 : windowWidth < 480 ? 80 : 100,
        background: pastelColors.accent,
        borderRadius: "50%",
        opacity: 0.4
      }} />

      <div style={{
        position: "absolute",
        bottom: windowHeight < 600 ? -40 : windowWidth < 480 ? -60 : -80,
        left: windowHeight < 600 ? -30 : windowWidth < 480 ? -45 : -60,
        width: windowHeight < 600 ? 70 : windowWidth < 480 ? 100 : 120,
        height: windowHeight < 600 ? 70 : windowWidth < 480 ? 100 : 120,
        background: pastelColors.secondary,
        borderRadius: "50%",
        opacity: 0.3
      }} />

      <div style={{ position: "relative", zIndex: 2 }}>
        <div style={{ textAlign: "center", marginBottom: getTopMargin() }}>
          <h2 style={{
            color: pastelColors.text,
            fontWeight: 600,
            fontSize: windowHeight < 600 ? "16px" : windowWidth < 480 ? "18px" : windowWidth < 768 ? "20px" : "22px",
            background: "linear-gradient(135deg, #8b7ba6 0%, #6d5b8e 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent"
          }}>
            Chat
          </h2>
          <div style={{ fontSize: windowHeight < 600 ? "10px" : windowWidth < 480 ? "11px" : "12px", color: "#b8a9cc" }}>
            reliable & Secure Messaging
          </div>
        </div>

        <div style={{
          height: getChatHeight(),
          overflowY: "auto",
          padding: "14px",
          background: "rgba(246, 227, 227, 0.8)",
          borderRadius: "18px",
          border: "1px solid rgba(232,223,245,0.6)",
          marginBottom: "18px"
        }}>
          {messages.length === 0 && (
            <div style={{ textAlign:"center", marginTop: "60px", color:"#b8a9cc" }}>
              Your messages will appear here…
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} style={{ display:"flex", flexDirection:"column", alignItems: msg.from==="you"?"flex-end":"flex-start", margin:"10px 0" }}>
              <span style={{
                background: msg.from==="you"?pastelColors.yourMessage:pastelColors.botMessage,
                padding:"10px 16px",
                borderRadius: msg.from==="you"?"14px 14px 4px 14px":"14px 14px 14px 4px",
                fontSize:"14px",
                color:pastelColors.text,
                maxWidth:getMessageMaxWidth(),
                wordBreak:"break-word"
              }}>{msg.text}</span>
              <div style={{ fontSize:"10px", marginTop:"3px", color:"#b8a9cc" }}>{msg.timestamp}</div>
            </div>
          ))}
          <div ref={messagesEndRef}/>
        </div>

        <div style={{ display:"flex", gap:"8px" }}>
          <input
            value={message}
            onChange={(e)=>setMessage(e.target.value)}
            onKeyDown={(e)=>e.key==="Enter" && sendMessage()}
            placeholder="Type a soft message…"
            style={{ flex:1, padding:"14px", borderRadius:"16px", border:"1px solid #d8cfea" }}
          />

          <button
            onClick={sendMessage}
            disabled={!message.trim()}
            style={{
              padding:"14px 20px",
              borderRadius:"16px",
              background: message.trim() ? pastelColors.primary : "#e7bdbdff",
              color:"white",
              border:"none",
              cursor: message.trim()?"pointer":"not-allowed"
            }}
          >
            ➤ Send
          </button>
        </div>

        {/* ✅ Clear chat button */}
        <div style={{ textAlign:"center", marginTop:"12px" }}>
          <button onClick={clearChat} style={{
            background:"none",
            border:"none",
            color:"#9b88b1",
            fontSize:"12px",
            cursor:"pointer"
          }}>Clear Chat History</button>
        </div>
      </div>
    </div>
  );
}

export default ChatApp;
