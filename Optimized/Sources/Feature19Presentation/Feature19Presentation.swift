import Feature19Domain
import Feature19Data

public enum Feature19PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature19DomainModel = Feature19DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
