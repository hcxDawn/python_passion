var ocrDemo = {
    CANVAS_WIDTH: 200,
    TRANSLATED_WIDTH: 20,
    PIXEL_WIDTH: 10,
    data: new Array(400),
    trainArray: [],
    BATCH_SIZE: 1,
    HOST: "http://127.0.0.1",
    PORT: "4567",
    
    drawGrid: function(ctx) {
        for (var x = this.PIXEL_WIDTH, y = this.PIXEL_WIDTH; 
                 x < this.CANVAS_WIDTH; x += this.PIXEL_WIDTH, 
                 y += this.PIXEL_WIDTH) {
            ctx.strokeStyle = "#000000";
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, this.CANVAS_WIDTH);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(this.CANVAS_WIDTH, y);
            ctx.stroke();
        }
    },
    
    onMouseMove: function(e, ctx, canvas) {
        if (!canvas.isDrawing) {
            return;
        }
        this.fillSquare(ctx, 
            e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    },

    onMouseDown: function(e, ctx, canvas) {
        canvas.isDrawing = true;
        this.fillSquare(ctx, 
            e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    },

    onMouseUp: function(e, ctx, canvas) {
        canvas.isDrawing = false;
    },

    fillSquare: function(ctx, x, y) {
        var xPixel = Math.floor(x / this.PIXEL_WIDTH);
        var yPixel = Math.floor(y / this.PIXEL_WIDTH);
        this.data[((xPixel - 1)  * this.TRANSLATED_WIDTH + yPixel) - 1] = 1;
        
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(xPixel * this.PIXEL_WIDTH, yPixel * this.PIXEL_WIDTH, 
            this.PIXEL_WIDTH, this.PIXEL_WIDTH);
    },
    
    train: function() {
        var digitVal = document.getElementById("digit").value;
        if (!digitVal || this.data.indexOf(1) < 0) {
            alert("Please type and draw a digit value in order to train the network");
            return;
        }
        this.trainArray = {"data": this.data, "label": parseInt(digitVal)};

        var jsonContent = {
            trainArray: this.trainArray,
            train: true
        };
        console.log(jsonContent);
        this.sendData(jsonContent);
    },
    
    receiveResponse: function(xmlHttp) {
        console.log("receiveResponse enter, status" + xmlHttp.status);
        console.log(xmlHttp)
        if (xmlHttp.status != 200) {
            alert("Server returned status " + xmlHttp.status);
            return;
        }
        var responseJSON = JSON.parse(xmlHttp.responseText);
        if(responseJSON){
            if(responseJSON["type"] == "predict")
            {
                console.log("result %d", responseJSON["result"]);
            }
            else if(responseJSON["type"] == "train")
            {
                console.log("result OK");
            }
            return;
        }
        alert("something unknown error happen");
    },

    onError: function(e) {
        console.log(e.target);
    },

    sendData: function(json) {
        var xmlHttp = new XMLHttpRequest();
        var msg = JSON.stringify(json);

        xmlHttp.open('POST', this.HOST + ":" + this.PORT, true);
        xmlHttp.onload = function() { this.receiveResponse(xmlHttp); }.bind(this);
        xmlHttp.onerror = function(e) { this.onError(e); }.bind(this);
        xmlHttp.send(msg);
    },

    resetCanvas: function() {
        var cvs = document.getElementById("canvas");
        var ctx = cvs.getContext("2d");
        ctx.clearRect(0, 0, ctx.width, ctx.height);
        this.drawGrid(ctx);
    },

    predict: function () {
        if (this.data.indexOf(1) < 0) {
            alert("Please type and draw a digit value in order to train the network");
            return;
        }
        this.trainArray = {"data": this.data, "label": 101};
        var jsonContent = {
            trainArray: this.trainArray,
            train: false
        };
        console.log(jsonContent);
        this.sendData(jsonContent);
    },

    onLoadFunction: function(){
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
        this.drawGrid(ctx);
        for(var i=0; i<this.data.length; i++)
            this.data[i] = 0;

        canvas.onmousedown = function(e){
            this.onMouseDown(e, ctx, canvas);
        }.bind(this);
        canvas.onmousemove = function(e){
            this.onMouseMove(e, ctx, canvas);
        }.bind(this);
        canvas.onmouseup = function(e){
            this.onMouseUp(e, ctx, canvas);
        }.bind(this);
    }
}