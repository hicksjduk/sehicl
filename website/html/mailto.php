<?php
class Mailto
{
	private $id;
	private $domain;
	private $description = null;
	
	function __construct($id, $domain=null)
	{
		$this->id = $id;
		$this->domain = $domain;
	}
	
	function setDescription($description)
	{
		$this->description = $description;
		return $this;
	}
	
	function getMailtoCall($linkText=null)
	{
		$dom = $this->domain == null ? "\"\"" : "\"$this->domain\"";
		$descr = $this->description == null ? "\"\"" : "\"$this->description\"";
		$link = $linkText == null ? "\"\"" : "\"$linkText\"";
		return "<script>document.write(mailTo(\"$this->id\", $dom, $descr, $link));</script>";
	}
}