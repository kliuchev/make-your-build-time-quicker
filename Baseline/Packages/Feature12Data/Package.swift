// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature12Data",
    products: [.library(name: "Feature12Data", targets: ["Feature12Data"])],
    dependencies: [.package(path: "../Feature12Domain")],
    targets: [.target(name: "Feature12Data", dependencies: [.product(name: "Feature12Domain", package: "Feature12Domain")])]
)
