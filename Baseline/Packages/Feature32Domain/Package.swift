// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature32Domain",
    products: [.library(name: "Feature32Domain", targets: ["Feature32Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature32Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
