export const getNewsAnalysis = (text) => {
    if(text.includes("bad")){
        return `${text} - ${"bad"}`;
    }
    return `${text} - ${"good"}`;
};