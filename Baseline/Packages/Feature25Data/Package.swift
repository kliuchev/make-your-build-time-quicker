// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature25Data",
    products: [.library(name: "Feature25Data", targets: ["Feature25Data"])],
    dependencies: [.package(path: "../Feature25Domain")],
    targets: [.target(name: "Feature25Data", dependencies: [.product(name: "Feature25Domain", package: "Feature25Domain")])]
)
